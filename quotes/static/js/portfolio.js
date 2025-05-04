document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('portfolioModal');
  const portfolioItems = document.querySelectorAll('.portfolio-item');

  if (modal && portfolioItems) {
    const modalImage = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalDescription = document.getElementById('modalDescription');
    const closeBtn = document.querySelector('.portfolio-modal-close');

    // Function to open modal
    function openModal(item) {
      const thumbnail = item.querySelector('.portfolio-image');
      const fullSizeUrl = thumbnail.dataset.fullSrc;
      const title = item.querySelector('.portfolio-item-title').textContent;
      const description = item.querySelector('.portfolio-item-description').textContent;

      // Show loading state
      modalImage.src = thumbnail.src; // Show thumbnail first
      modalTitle.textContent = title;
      modalDescription.textContent = description;
      modal.classList.add('portfolio-modal-active');
      document.body.style.overflow = 'hidden';

      // Load full-size image
      const fullSizeImage = new Image();
      fullSizeImage.onload = function () {
        modalImage.src = fullSizeUrl;
      };
      fullSizeImage.src = fullSizeUrl;
    }

    // Function to close modal
    function closeModal() {
      modal.classList.remove('portfolio-modal-active');
      document.body.style.overflow = 'auto';
    }

    // Add event listeners to gallery items
    portfolioItems.forEach((item) => {
      item.addEventListener('click', function () {
        openModal(this);
      });
    });

    // Close modal when clicking close button
    closeBtn.addEventListener('click', closeModal);

    // Close modal when clicking outside of content
    modal.addEventListener('click', function (e) {
      if (e.target === modal) {
        closeModal();
      }
    });

    // Close modal when pressing Escape key
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.classList.contains('portfolio-modal-active')) {
        closeModal();
      }
    });
  }
});
