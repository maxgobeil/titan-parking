document.addEventListener('DOMContentLoaded', function () {
  // Get mobile dropdown button
  const mobileDropBtn = document.querySelector('.mobile-dropbtn');
  const mobileDropContent = document.querySelector('.mobile-dropdown-content');

  if (mobileDropBtn && mobileDropContent) {
    mobileDropBtn.addEventListener('click', function (e) {
      e.preventDefault();
      mobileDropContent.classList.toggle('show');

      // Rotate icon when dropdown is toggled
      const icon = this.querySelector('.icon-chevron-down');
      if (icon) {
        if (mobileDropContent.classList.contains('show')) {
          icon.style.transform = 'rotate(180deg)';
        } else {
          icon.style.transform = 'rotate(0)';
        }
      }
    });
  }
});
