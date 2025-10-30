// Sidebar
/* global bootstrap: false */
(function () {
  'use strict'
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.forEach(function (tooltipTriggerEl) {
    new bootstrap.Tooltip(tooltipTriggerEl)
  })
})()


// Change sidebar width on window resize
$( window ).on( "resize", function() {
  if(window.innerWidth <= 991) {
    $('#sidebar').addClass('collapsed').removeClass('opened');
  } else {
    $('#sidebar').removeClass('collapsed').removeClass('opened');
  }
} );

$(document).ready(function () {
  // Add 'collapsed' class if window width is less than or equal to 991px
  if(window.innerWidth <= 991) {
    $('#sidebar').addClass('collapsed');
  }

  $('#sidebarToggle').click(function () {
    // If 'collapsed' class exists, remove it and adjust navbar classes
    // Else, add 'collapsed' class and remove 'opened' class, then adjust navbar classes
    if ($('#sidebar').hasClass('collapsed')) {
      $('#sidebar').removeClass('collapsed').addClass('opened');
      $('#navbar').addClass('navbar-with-sidebar').removeClass('navbar-full');
    } else {
      $('#sidebar').addClass('collapsed').removeClass('opened');
      $('#navbar').addClass('navbar-full').removeClass('navbar-with-sidebar');
    }
  });

  // Add copy buttons to code blocks
  addCopyButtons();
});

function addCopyButtons() {
  // Find all code blocks within pre tags
  const codeBlocks = document.querySelectorAll('pre > code[class^="language-"]');

  codeBlocks.forEach((codeBlock) => {
    const preElement = codeBlock.parentElement;

    // Skip if button already exists
    if (preElement.querySelector('.copy-code-btn')) {
      return;
    }

    // Create copy button
    const copyButton = document.createElement('button');
    copyButton.className = 'copy-code-btn';
    copyButton.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
      </svg>
      <span>Copy</span>
    `;

    // Add click handler
    copyButton.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();

      const code = codeBlock.textContent;

      // Copy to clipboard
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(code).then(() => {
          // Update button state
          copyButton.classList.add('copied');
          copyButton.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span>Copied!</span>
          `;

          // Reset after 2 seconds
          setTimeout(() => {
            copyButton.classList.remove('copied');
            copyButton.innerHTML = `
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <span>Copy</span>
            `;
          }, 2000);
        }).catch(err => {
          console.error('Failed to copy code:', err);
          alert('Failed to copy code to clipboard');
        });
      } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = code;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        document.body.appendChild(textArea);
        textArea.select();
        try {
          document.execCommand('copy');
          copyButton.classList.add('copied');
          copyButton.textContent = 'Copied!';
          setTimeout(() => {
            copyButton.classList.remove('copied');
            copyButton.textContent = 'Copy';
          }, 2000);
        } catch (err) {
          console.error('Failed to copy code:', err);
          alert('Failed to copy code to clipboard');
        }
        document.body.removeChild(textArea);
      }
    });

    // Append button to pre element
    preElement.appendChild(copyButton);
  });
}