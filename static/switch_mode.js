$(document).ready(function() {
  // Check and apply the mode from cookie
  const mode = getCookie('theme') || 'light'; // Default to 'light' if no cookie
  applyTheme(mode);

  // Toggle theme between light and dark
  $('#theme-toggle').on('change', function() {
      const newMode = this.checked ? 'dark' : 'light';
      applyTheme(newMode);
      setCookie('theme', newMode, 365); // Store the preference for 365 days
  });

  $('#image-toggle').on('click', function() {
    const theme = $('#theme-toggle').is(':checked') ? 'dark' : 'light';
    const imageUrl = theme === 'dark' ? '/static/NGA-Tables_dark.svg' : '/static/NGA-Tables_light.svg';
    window.open(imageUrl, '_blank');
    });
  // Function to apply the theme to HTML and DataTables
  function applyTheme(theme) {
      let html = document.querySelector('html');
      if (theme === 'dark') {
          html.classList.add('dark-mode');
          html.setAttribute('data-bs-theme', 'dark');
          $('#theme-toggle').prop('checked', true);
      } else {
          html.classList.remove('dark-mode');
          html.setAttribute('data-bs-theme', 'light');
          $('#theme-toggle').prop('checked', false);
      }
  }

  // Function to set a cookie
  function setCookie(name, value, days) {
      const expires = "expires=" + new Date(Date.now() + days * 864e5).toUTCString();
      document.cookie = name + "=" + (value || "") + ";" + expires + ";path=/";
  }

  // Function to get a cookie value
  function getCookie(name) {
      const nameEQ = name + "=";
      const ca = document.cookie.split(';');
      for(let i = 0; i < ca.length; i++) {
          let c = ca[i];
          while (c.charAt(0) === ' ') c = c.substring(1);
          if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
      }
      return null;
  }

});