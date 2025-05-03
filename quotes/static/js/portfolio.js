document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('portfolioModal');
  const portfolioItems = document.querySelectorAll('.portfolio-item');

  if (modal && portfolioItems) {
    const modalImage = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalDescription = document.getElementById('modalDescription');
    const closeBtn = document.querySelector('.portfolio-modal-close');

    // Function to open modal
    function openModal(image, title, description) {
      modalImage.src = image;
      modalImage.alt = title;
      modalTitle.textContent = title;
      modalDescription.textContent = description;
      modal.classList.add('portfolio-modal-active');
      document.body.style.overflow = 'hidden';
    }

    // Function to close modal
    function closeModal() {
      modal.classList.remove('portfolio-modal-active');
      document.body.style.overflow = 'auto';
    }

    // Add event listeners to gallery items
    portfolioItems.forEach((item) => {
      item.addEventListener('click', function () {
        const image = this.querySelector('.portfolio-image').src;
        const title = this.querySelector('.portfolio-item-title').textContent;
        const description = this.querySelector('.portfolio-item-description').textContent;
        openModal(image, title, description);
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
