---
layout: page
tags: [Image]
page_title: Community Images
---

OpenStack Community Images are images that are shared across all OpenStack projects. This allows users to use images that are  
maintained by the community and not by the OpenStack provider. These community images provide a great way to share your own creations with other users.

## Using a Community Image
Before you decide to use a community image, you should be aware of the risks of using a community image.  
You can read more about the risks of using a community image in the [Risks of Using Community Images](#risks-of-using-community-images) section.

Using a community image is as simple as using an image provided by the provider or by yourself. You can use a community image  
by going to the `Compute` > `Instances` tab. Then click on the `Launch Instance` button to create a new instance. On the `Source` tab,  
you can select the community image you want to use. Community images are shown as `Community` in the `Visibility` column.

## Creating a Community Image
> Warning: Be aware that when you share an image with the community, you are sharing it with all users on the platform of the OpenStack provider.

When you want to create a community image, you need to upload an image to OpenStack and then share it with the community by setting the visibility to `Community`.  
You can do this by logging in to the OpenStack Dashboard and going to the `Compute` > `Images` tab. Then click on the `Create Image` button to create a new image.  
How you want   or need to configure your image does not really matter; the only thing you are required to do is set the `Visibility` to `Community` to make the image a community image.

> Note: Some providers may have disabled community image creation by default. If you want to create a community image, you may have to contact their support.  
Providers do this mainly to protect their users from malicious images by first checking the creators of the images before allowing them to create community images.

## Deleting a Community Image
When a community image is no longer needed, it may be deleted by the owner of the image. Sadly, this will also delete the image for all other users who are using it.  
If you are currently running on a community image and it gets deleted, your instance will keep running on the image. However, if you want to rebuild or spawn a  
new instance with the same image, you will not be able to do this since the image is not available anymore.

Deleting a community image is done by the owner of the image. This can be done by going to the `Images` tab in the OpenStack Dashboard and clicking  
on the `Delete Image` button behind the image you want to delete.

## Risks of Using Community Images
When you use community images, you are trusting the owner of the image. The owner of the image can do anything with the image, and you  
will not be able to see what the owner has done with the image. This means that the owner of the image can do anything with the  
image, including but not limited to:
- Installing malware on the image.
- Installing viruses on the image.
- Installing backdoors on the image.
- Installing keyloggers on the image.

Using community images does not mean that you are automatically exploited. Most users create awesome and safe images you can use, but you should  
always stay aware of the risks community images bring with them. If you want to be sure that the image is safe, you can always use the images  
provided by the OpenStack provider or create your own images and use those.

## Support for Community Images
Sadly, support for community images at most providers is not included. If you have any issues with a community image, please contact the owner of the image.  
Most of the time, the owner of the image will be able to help you with your issue. If the owner of the image is not able to help you with your issue, you  
can always contact the support team of the OpenStack provider. However, the support of the OpenStack provider may not be able to help you with your issue  
because they have not created the image.