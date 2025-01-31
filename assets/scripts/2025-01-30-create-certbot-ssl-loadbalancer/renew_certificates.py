import os
import re
import base64
from datetime import datetime
import argparse
import openstack
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509 import load_pem_x509_certificate
import certbot.main


class CertificateRenewer:
    def __init__(self):
        # Parse command line arguments
        parser = argparse.ArgumentParser(
            description="""
Licensed under the Apache License, Version 2.0 (the "License")
Version 1.0 (2025-01-30)
This script is used to renew the OpenStack certificate using certbot and upload it to Barbican.
It also updates the Octavia listener with the new certificate.

Depends on clouds.yaml for OpenStack credentials, and certbot-dns-openstack plugin for DNS challenge.
The script will use the certbot-dns-openstack plugin to authenticate the domain ownership and renew the certificate.
It assumes that the certificate is stored in /etc/letsencrypt/live/<domain>/ directory.
It depends on OpenStack designate for DNS challenge, and OpenStack Barbican for storing the certificate.
DNS for the domain needs to be configured for the domain to use the OpenStack DNS service.

"""
        )
        parser.add_argument(
            "--domain",
            default=None,
            help="The domain for which to renew the certificate. Multi domain is currently not supported, wildcard domain is supported",
        )
        parser.add_argument(
            "--os-cloud",
            help="OpenStack cloud name",
        )
        parser.add_argument(
            "--renew",
            action="store_true",
            help="Enable certbot renewal, if not set, the script will search for certificates to use in Barbican and update Octavia listener",
        )
        parser.add_argument(
            "--force-renewal",
            action="store_true",
            help="Force renewal of certificate with certbot even if expiration date is not near",
        )
        parser.add_argument(
            "--email",
            help="Email address for certbot",
        )
        parser.add_argument(
            "--create-barbican-secret",
            action="store_true",
            help="Upload the certificate to Barbican if the certificate is not already uploaded (based on subject, '_full_cert_expiring_' and expiration date)",
        )
        parser.add_argument(
            "--octavia-listener",
            nargs="+",
            default=[],
            help="Add all listener IDs to update with new certificate (will fallback to SNI listener update if certificate subject mismatch, use --force-rename to force update)",
        )
        parser.add_argument(
            "--octavia-sni-listener",
            nargs="+",
            default=[],
            help="Add all SNI listener IDs to update with new certificate",
        )
        parser.add_argument(
            "--force-reupload",
            action="store_true",
            help="Force re-uploading certificate to Barbican, will update Barbican with the certificate even if it already exists",
        )
        parser.add_argument(
            "--force-rename",
            action="store_true",
            help="Force changing hostname in octavia",
        )
        parser.add_argument(
            "--cleanup-barbican",
            action="store_true",
            help="Cleanup old certificates in Barbican",
        )
        parser.add_argument(
            "--cleanup-sni",
            action="store_true",
            help="Cleanup old SNI certificates in Octavia",
        )
        parser.add_argument(
            "--key-path",
            default=None,
            help="Path to the key file to manually upload the certificate",
        )
        parser.add_argument(
            "--chain-path",
            default=None,
            help="Path to the chain file to manually upload the certificate",
        )
        parser.add_argument(
            "--fullchain-path",
            default=None,
            help="Path to the fullchain file to manually upload the certificate",
        )
        parser.add_argument(
            "--p12-path",
            default=None,
            help="Path to the p12 file to manually upload the certificate",
        )

        self.args = parser.parse_args()
        if not self.args.os_cloud:
            self.args.os_cloud = os.environ.get("OS_CLOUD", None)
            if not self.args.os_cloud:
                raise ValueError(
                    "OpenStack cloud name is required, use --os-cloud or set OS_CLOUD environment variable"
                )

        if self.args.domain:
            self.domain = self.args.domain
            # Validate domain name
            domain_regex = re.compile(
                r"^(?:\*\.)?"  # Optional wildcard prefix
                r"(?:[a-zA-Z0-9]"  # First character of the domain
                r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)"  # Sub domain + hostname
                r"+[a-zA-Z]{2,6}$"  # First level TLD
            )

            if not domain_regex.match(self.domain):
                raise ValueError(f"Invalid domain name: {self.domain}")
            self.stripped_domain = self.domain.replace("*.", "")
            self.privkey_path = (
                f"/etc/letsencrypt/live/{self.stripped_domain}/privkey.pem"
            )
            self.fullchain_path = (
                f"/etc/letsencrypt/live/{self.stripped_domain}/fullchain.pem"
            )
            self.chain_path = f"/etc/letsencrypt/live/{self.stripped_domain}/chain.pem"
            self.p12_path = f"/etc/letsencrypt/live/{self.stripped_domain}/complete.p12"

        else:
            if (
                self.args.key_path
                and self.args.chain_path
                and self.args.fullchain_path
                and self.args.p12_path
            ):
                self.privkey_path = self.args.key_path
                self.fullchain_path = self.args.fullchain_path
                self.chain_path = self.args.chain_path
                self.p12_path = self.args.p12_path
                self.domain = None
            else:
                raise ValueError("Domain name or all certificate files are required")
        self._conn = None

    def get_connection(self):
        if self._conn is None:
            self._conn = openstack.connect(cloud=self.args.os_cloud)
        return self._conn

    def renew_certificate(self):
        if self.args.renew and not self.args.key_path:
            print(f"Renewing domain: {self.domain} with certbot")
            # check for the version of certbot
            if certbot.__version__ >= "1.0":
                certbot_args = [
                    "certonly",
                    "--non-interactive",
                    "--agree-tos",
                    "--authenticator",
                    "dns-openstack",
                    "--dns-openstack-cloud",
                    self.args.os_cloud,
                    "-d",
                    self.domain,
                ]
                if self.args.email:
                    certbot_args.extend(["--email", self.args.email])
                if self.args.force_renewal:
                    certbot_args.append("--force-renewal")
                certbot.main.main(certbot_args)
            else:
                certbot_args = [
                    "certonly",
                    "--non-interactive",
                    "--agree-tos",
                    "--authenticator",
                    "certbot-dns-openstack:dns-openstack",
                    "--certbot-dns-openstack:dns-openstack-cloud",
                    self.args.os_cloud,
                    "-d",
                    self.domain,
                ]
                if self.args.email:
                    certbot_args.extend(["--email", self.args.email])
                if self.args.force_renewal:
                    certbot_args.append("--force-renewal")
                certbot.main.main(certbot_args)

    def get_used_certificates(self):
        conn = self.get_connection()
        used_certificates = []
        for listener in conn.load_balancer.listeners():
            if listener.default_tls_container_ref:
                used_certificates.append(listener.default_tls_container_ref)
            if listener.sni_container_refs:
                used_certificates.extend(listener.sni_container_refs)
        return used_certificates

    def cleanup_barbican(self):
        used_certificates = self.get_used_certificates()
        today = datetime.now()
        conn = self.get_connection()
        certificates = conn.key_manager.secrets()
        for certificate in certificates:
            if certificate.id in used_certificates:
                print(f"Skipping in-use certificate: {certificate.name}")
                continue
            if certificate.name.startswith(f"{self.domain}_full_cert_expiring_"):
                if certificate.id == self.certificate_url:
                    print(f"Skipping certificate: {certificate.name}")
                    continue
                expiration_date = datetime.fromisoformat(
                    certificate.name.split("_")[-1]
                )
                if expiration_date < today:
                    print(f"Deleting certificate: {certificate.name}")
                    conn.key_manager.delete_secret(
                        certificate.id.split("/")[-1], ignore_missing=False
                    )
                else:
                    print(f"Certificate {certificate.name} is not expired")

    def get_cert_from_p12(self, certificate_data):
        # get the certificate from pkcs12 certificate binary data
        secret_payload = pkcs12.load_pkcs12(certificate_data, password=None)
        cert = secret_payload.cert.certificate
        return cert

    def get_cert_from_barbican(self, certificate_url):
        conn = self.get_connection()
        certificate_id = certificate_url.split("/")[-1]
        secret = conn.key_manager.get_secret(certificate_id)
        if not secret:
            print(f"Failed to get secret for {certificate_url}")
            return None
        secret_data = conn.key_manager.get(
            f"{certificate_url}/payload",
            headers={"accept": secret.payload_content_type},
            skip_cache=False,
        )
        if not secret_data:
            print(f"Failed to get secret data for {certificate_url}")
            return None
        cert_obj = self.get_cert_from_p12(secret_data.content)
        return cert_obj

    def create_pkcs12_file(self, dest_path):
        with open(self.privkey_path, "rb") as key_file, open(
            self.fullchain_path, "rb"
        ) as cert_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(), password=None
            )
            certificate = load_pem_x509_certificate(cert_file.read())
            intermediate_certificates = []
            with open(self.chain_path, "rb") as chain_file:
                chain_data = chain_file.read().decode("utf-8")
                intermediate_certificates_pem = re.findall(
                    r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----",
                    chain_data,
                    re.DOTALL,
                )
                intermediate_certificates = [
                    load_pem_x509_certificate(cert.encode("utf-8"))
                    for cert in intermediate_certificates_pem
                ]
            p12_data = pkcs12.serialize_key_and_certificates(
                name=b"certificate",
                key=private_key,
                cert=certificate,
                cas=intermediate_certificates,
                encryption_algorithm=serialization.NoEncryption(),
            )
            with open(dest_path, "wb") as p12_file:
                p12_file.write(p12_data)

        return certificate

    def get_existing_secret(self, name) -> str:
        conn = self.get_connection()
        if self.args.force_reupload:
            return None
        secrets = conn.key_manager.secrets()
        for secret in secrets:
            if secret.name == name:
                return secret.id
        return None

    def store_secret_in_openstack(self, p12_path, name, expiration_date):
        """Function to store the certificate in OpenStack Barbican
        Currently, the certificate expiration date is not being stored in Barbican due to bug in octavia
        https://bugs.launchpad.net/octavia/+bug/2096920"""
        conn = self.get_connection()
        existing_secret = self.get_existing_secret(name)
        if existing_secret:
            print(
                f"Certificate {name} already exists in Barbican with URL: {existing_secret}"
            )
            return existing_secret

        with open(p12_path, "rb") as cert_file:
            cert_data = base64.b64encode(cert_file.read()).decode("utf-8")

        secret = conn.key_manager.create_secret(
            name=name,
            payload=cert_data,
            payload_content_type="application/octet-stream",
            payload_content_encoding="base64",
        )

        self.certificate_url = secret.secret_ref
        print(f"Barbican certificate url: {self.certificate_url}")
        return self.certificate_url

    def update_octavia_listener(self, certificate_url):
        conn = self.get_connection()
        for listener_id in self.args.octavia_listener:
            listener = conn.load_balancer.get_listener(listener_id)
            if listener.default_tls_container_ref == certificate_url:
                print(
                    f"Listener {listener.name} already has the certificate, not updating"
                )
                continue
            if not self.args.force_rename:
                current_certificate = self.get_cert_from_barbican(
                    listener.default_tls_container_ref
                )
                updated_certificate = self.get_cert_from_barbican(certificate_url)
                current_subject = (
                    current_certificate.subject.rfc4514_string()
                    .split(",")[0]
                    .split("=")[1]
                )
                updated_subject = (
                    updated_certificate.subject.rfc4514_string()
                    .split(",")[0]
                    .split("=")[1]
                )
                if not current_subject == updated_subject:
                    print(f"Certificate subject mismatch for listener {listener.name}")
                    print(
                        f"Current certificate: {current_subject}, Updated certificate: {updated_subject}"
                    )
                    print(f"Falling back to sni listener update")
                    self.args.octavia_sni_listener.append(listener_id)
                    continue

            print(f"Updating listener {listener.name} with new certificate")
            conn.load_balancer.update_listener(
                listener_id, default_tls_container_ref=certificate_url
            )

    def update_octavia_sni_listener(self, certificate_url):
        conn = self.get_connection()
        print(
            f"Updating SNI listeners with new certificate{self.args.octavia_sni_listener}"
        )
        for listener_id in self.args.octavia_sni_listener:
            listener = conn.load_balancer.get_listener(listener_id)
            if (
                listener.sni_container_refs
                and certificate_url in listener.sni_container_refs
            ):
                print(
                    f"Listener {listener.name} already has the certificate, not updating"
                )
                continue
            print(f"Updating SNI listener {listener.name} with new certificate")
            sni_container_refs = listener.sni_container_refs or []
            sni_container_refs.append(certificate_url)
            for cert in sni_container_refs:
                if not self.get_cert_from_barbican(cert):
                    print(f"Certificate {cert} not found in Barbican, skipping")
                    sni_container_refs.remove(cert)
            conn.load_balancer.update_listener(
                listener_id, sni_container_refs=sni_container_refs
            )

    def cleanup_octavia_sni(self):
        conn = self.get_connection()
        for listener in conn.load_balancer.listeners():
            if not listener.sni_container_refs:
                continue
            print(f"Cleaning up SNI for listener {listener.name}")
            updated_snis = []
            expired_certs = []
            latest_certs = {}
            for certificate in listener.sni_container_refs:
                secret = conn.key_manager.get_secret(certificate.split("/")[-1])
                cert_obj = self.get_cert_from_barbican(certificate)
                if not cert_obj:
                    print(f"Failed to get certificate for {certificate}")
                    continue

                expires = cert_obj.not_valid_after.isoformat()
                subject = cert_obj.subject.rfc4514_string().split(",")[0].split("=")[1]
                if subject not in latest_certs:
                    latest_certs[subject] = {
                        "expires": expires,
                        "secret": secret,
                        "url": certificate,
                    }
                elif expires > latest_certs[subject]["expires"]:
                    expired_certs.append(latest_certs[subject]["secret"])
                    latest_certs[subject] = {
                        "expires": expires,
                        "secret": secret,
                        "url": certificate,
                    }
                else:
                    expired_certs.append(secret)
            for cert in latest_certs:
                updated_snis.append(latest_certs[cert]["url"])

            for cert in expired_certs:
                print(f"Removing certificate: {cert.id}")
            if updated_snis != listener.sni_container_refs and len(updated_snis) > 0:
                print(f"Updating SNI for listener {listener.name}")
                print(f"Old SNI: {listener.sni_container_refs}")
                print(f"New SNI: {updated_snis}")
                conn.load_balancer.update_listener(
                    listener.id, sni_container_refs=updated_snis
                )

    def run(self):
        self.renew_certificate()
        self.certificate_url = None
        certificate = self.create_pkcs12_file(self.p12_path)
        if not self.domain:
            self.domain = (
                certificate.subject.rfc4514_string().split(",")[0].split("=")[1]
            )
            self.stripped_domain = self.domain.replace("*.", "")
        print(f"input domain: {self.domain}, stripped domain: {self.stripped_domain}")

        name = f"{self.domain}_full_cert_expiring_{certificate.not_valid_after.strftime('%Y-%m-%d')}"
        expiration_date = certificate.not_valid_after.isoformat()
        print(
            f"Expiration date: {expiration_date}, Domain: {self.domain}, Name: {name}"
        )

        if self.args.create_barbican_secret:
            certificate_url = self.store_secret_in_openstack(
                self.p12_path, name, expiration_date
            )
        if self.args.octavia_listener:
            if not certificate_url:
                certificate_url = self.get_existing_secret(name)
            if certificate_url:
                self.update_octavia_listener(certificate_url)
            else:
                print(
                    "Skipping Octavia listener update as Barbican secret is not created, and not found"
                )
                print("Use --create-barbican-secret to create Barbican secret")
        if self.args.octavia_sni_listener:
            if not certificate_url:
                certificate_url = self.get_existing_secret(name)
            if certificate_url:
                self.update_octavia_sni_listener(certificate_url)
            else:
                print(
                    "Skipping Octavia SNI listener update as Barbican secret is not created, and not found"
                )
                print("Use --create-barbican-secret to create Barbican secret")

        if self.args.cleanup_sni:
            self.cleanup_octavia_sni()
        if self.args.cleanup_barbican:
            self.cleanup_barbican()


if __name__ == "__main__":
    renewer = CertificateRenewer()
    renewer.run()
