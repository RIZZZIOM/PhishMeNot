// Function to navigate to the next step in the wizard
function nextStep(currentStep) {
    document.getElementById(`step${currentStep}`).style.display = 'none';
    document.getElementById(`step${currentStep + 1}`).style.display = 'block';
}

// Function to navigate to the previous step in the wizard
function prevStep(currentStep) {
    document.getElementById(`step${currentStep}`).style.display = 'none';
    document.getElementById(`step${currentStep - 1}`).style.display = 'block';
}

// Handle form submission
document.getElementById('campaignWizardForm').addEventListener('submit', function (event) {
    event.preventDefault();
    alert('Phishing campaign created and emails sent successfully!');
    // Add functionality to send campaign data to the backend
});
