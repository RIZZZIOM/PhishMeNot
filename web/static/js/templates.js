function previewTemplate(imageName) {
    // Remove any existing modal before creating a new one
    let existingModal = document.getElementById("imageModal");
    if (existingModal) {
        existingModal.remove();
    }

    // Create the modal dynamically
    let modal = document.createElement("div");
    modal.id = "imageModal";
    modal.className = "modal";
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <img id="modalImage" src="/static/images/${imageName}" alt="Template Preview">
        </div>
    `;

    // Append the modal to the body
    document.body.appendChild(modal);

    // Show the modal
    modal.style.display = "flex";

    // Close modal if user clicks outside the modal content
    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });
}

// Function to close the modal
function closeModal() {
    let modal = document.getElementById("imageModal");
    if (modal) {
        modal.remove(); // Completely remove modal from the DOM
    }
}
