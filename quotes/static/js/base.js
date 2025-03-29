document.addEventListener('DOMContentLoaded', function () {
  // Get references to menu elements
  const menuToggle = document.getElementById('menu-toggle');
  const menuClose = document.getElementById('menu-close');
  const mobileNav = document.getElementById('mobile-nav');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
  const header = document.querySelector('.header');
  const navLinks = document.querySelectorAll('.nav-link');
  const langButton = document.querySelector('.lang-button');

  const onScroll = () => {
    if (document.body.scrollTop > 100) {
      header.classList.add('scrolled');
      navLinks.forEach((link) => {
        link.classList.add('scrolled');
      });
      langButton.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
      navLinks.forEach((link) => {
        link.classList.remove('scrolled');
      });
      langButton.classList.remove('scrolled');
    }
  };
  // Toggle mobile menu
  function toggleMenu() {
    mobileNav.classList.toggle('open');
    document.body.classList.toggle('menu-open');
    menuToggle.style.display = mobileNav.classList.contains('open') ? 'none' : 'block';
  }

  // Event listeners for menu
  document.body.addEventListener('scroll', onScroll);
  if (menuToggle) menuToggle.addEventListener('click', toggleMenu);
  if (menuClose) menuClose.addEventListener('click', toggleMenu);

  // Close menu when clicking on mobile nav links
  mobileNavLinks.forEach((link) => {
    link.addEventListener('click', toggleMenu);
  });
});

function scrollToTop() {
  document.body.scrollTo({
    top: 0,
    behavior: 'smooth',
  });
}

document.getElementById('scroll-top-button').addEventListener('click', scrollToTop);
