document.addEventListener('DOMContentLoaded', function () {
  const savedLanguage = localStorage.getItem('preferredLanguage');
  if (savedLanguage) {
    // If there's a saved preference, make sure URL matches it
    const isEnglishPath = window.location.pathname.startsWith('/en/');

    if (savedLanguage === 'en' && !isEnglishPath) {
      // User prefers English but we're on French path
      const newPath = '/en' + window.location.pathname + window.location.hash;
      window.location.href = newPath;
    } else if (savedLanguage === 'fr' && isEnglishPath) {
      // User prefers French but we're on English path
      const newPath = window.location.pathname.slice(3) + window.location.hash;
      window.location.href = newPath;
    }
  }

  const langButtons = document.querySelectorAll('.lang-button');
  langButtons.forEach((button) => {
    button.addEventListener('click', () => {
      localStorage.setItem('preferredLanguage', button.value);
    });
  });

  const scrolledPages = [
    '/terms-of-service/',
    '/privacy-policy/',
    '/blog/',
    '/a-propos/',
    '/marquage-de-stationnement/',
    '/marquage-interieur/',
    '/marquage-au-sol/',
    '/marquage-personnalise/',
    '/restauration-de-lignes/',
    '/jeux-exterieurs/',
  ];
  const currentPath = window.location.pathname;
  const shouldBeScrolled = scrolledPages.some(
    (page) => currentPath.includes(page) || currentPath.endsWith(page.slice(0, -1)) // Handle with or without trailing slash
  );

  // Get references to menu elements
  const menuToggle = document.getElementById('menu-toggle');
  const menuClose = document.getElementById('menu-close');
  const mobileNav = document.getElementById('mobile-nav');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
  const header = document.querySelector('.header');
  const navLinks = document.querySelectorAll('.nav-link');
  const langButton = document.querySelector('.lang-button');

  if (shouldBeScrolled) {
    if (header) header.classList.add('scrolled');
    navLinks.forEach((link) => {
      link.classList.add('scrolled');
    });
    if (langButton) langButton.classList.add('scrolled');
  }

  const debouncedScroll = debounce(function () {
    if (document.body.scrollTop > 100) {
      header.classList.add('scrolled');
      navLinks.forEach((link) => {
        link.classList.add('scrolled');
      });
      if (langButton) langButton.classList.add('scrolled');
    } else if (!shouldBeScrolled) {
      header.classList.remove('scrolled');
      navLinks.forEach((link) => {
        link.classList.remove('scrolled');
      });
      if (langButton) langButton.classList.remove('scrolled');
    }
  }, 10);

  /*
  const onScroll = () => {
    if (document.body.scrollTop > 100) {
      header.classList.add('scrolled');
      navLinks.forEach((link) => {
        link.classList.add('scrolled');
      });
      if (langButton) langButton.classList.add('scrolled');
    } else if (!shouldBeScrolled) {
      // Only remove scrolled class if not on a legal page
      header.classList.remove('scrolled');
      navLinks.forEach((link) => {
        link.classList.remove('scrolled');
      });
      if (langButton) langButton.classList.remove('scrolled');
    }
  };*/

  document.body.addEventListener('scroll', debouncedScroll);
  if (menuToggle) menuToggle.addEventListener('click', toggleMenu);
  if (menuClose) menuClose.addEventListener('click', toggleMenu);

  // Toggle mobile menu
  function toggleMenu() {
    mobileNav.classList.toggle('open');
    document.body.classList.toggle('menu-open');
    menuToggle.style.display = mobileNav.classList.contains('open') ? 'none' : 'block';
  }

  function debounce(func, wait) {
    let timeout;
    return function () {
      const context = this;
      const args = arguments;
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(context, args), wait);
    };
  }

  // Close menu when clicking on mobile nav links
  mobileNavLinks.forEach((link) => {
    link.addEventListener('click', toggleMenu);
  });

  function scrollToTop() {
    document.body.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  }

  const scrollTopButton = document.getElementById('scroll-top-button');
  if (scrollTopButton) {
    scrollTopButton.addEventListener('click', scrollToTop);
  }
});
