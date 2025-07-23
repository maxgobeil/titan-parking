document.addEventListener('DOMContentLoaded', function () {
  // Get all mobile dropdown buttons
  const mobileDropBtns = document.querySelectorAll('.mobile-dropbtn');

  mobileDropBtns.forEach(function (mobileDropBtn) {
    const mobileDropContent = mobileDropBtn.nextElementSibling;

    if (mobileDropBtn && mobileDropContent) {
      mobileDropBtn.addEventListener('click', function (e) {
        e.preventDefault();

        // Close all other dropdowns first
        mobileDropBtns.forEach(function (otherBtn) {
          if (otherBtn !== mobileDropBtn) {
            const otherContent = otherBtn.nextElementSibling;
            const otherIcon = otherBtn.querySelector('.icon-chevron-down');

            if (otherContent) {
              otherContent.classList.remove('show');
            }
            if (otherIcon) {
              otherIcon.style.transform = 'rotate(0)';
            }
          }
        });

        // Toggle the clicked dropdown
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
});
