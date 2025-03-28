document.addEventListener('DOMContentLoaded', function () {
  // Get references to menu elements
  const menuToggle = document.getElementById('menu-toggle');
  const menuClose = document.getElementById('menu-close');
  const mobileNav = document.getElementById('mobile-nav');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
  const header = document.querySelector('.header');

  const onScroll = () => {
    if (document.body.scrollTop > 100) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };
  // Toggle mobile menu
  function toggleMenu() {
    mobileNav.classList.toggle('open');
    document.body.classList.toggle('menu-open');
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
