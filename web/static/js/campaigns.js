// Function to navigate to the next step in the wizard
function nextStep(currentStep) {
    const currentElement = document.getElementById(`step${currentStep}`);
    const nextElement = document.getElementById(`step${currentStep + 1}`);

    if (currentElement && nextElement) {
        currentElement.style.display = 'none';
        nextElement.style.display = 'block';
    }
}

// Function to navigate to the previous step in the wizard
function prevStep(currentStep) {
    const currentElement = document.getElementById(`step${currentStep}`);
    const prevElement = document.getElementById(`step${currentStep - 1}`);

    if (currentElement && prevElement) {
        currentElement.style.display = 'none';
        prevElement.style.display = 'block';
    }
}

// Handle campaign form submission
document.getElementById("campaignForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default form submission

    // Collect campaign details
    const campaignData = {
        template: document.getElementById("template").value + ".html", // Ensure correct file format
        campaignName: document.getElementById("campaignName").value.trim(),
        campaignDescription: document.getElementById("campaignDescription").value.trim(),
        senderEmail: document.getElementById("senderEmail").value.trim(),
        senderPassword: document.getElementById("senderPassword").value.trim(),
        emailTopic: document.getElementById("emailTopic").value.trim(),
        emailBody: document.getElementById("emailBody").value.trim(),
        ccEmails: document.getElementById("ccEmails")?.value.trim() || "",
        targetEmail: document.getElementById("targetEmail").value.trim() // Only one target email
    };

    // Validate required fields
    if (!campaignData.template || !campaignData.campaignName || !campaignData.senderEmail || !campaignData.senderPassword || !campaignData.emailTopic || !campaignData.emailBody || !campaignData.targetEmail) {
        alert("Error: Please fill in all required fields before submitting.");
        return;
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(campaignData.targetEmail)) {
        alert("Error: Invalid target email address.");
        return;
    }

    // Send API request to backend
    fetch("/api/send-campaign", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(campaignData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
        } else {
            alert("Error: " + (data.error || "Unknown error occurred"));
        }
    })
    .catch(error => {
        console.error("Error sending campaign:", error);
        alert("Failed to send campaign. Please check your settings and try again.");
    });
});

// Handle template selection and hosting
document.getElementById("template").addEventListener("change", function () {
    const selectedTemplate = this.value.trim();
    if (!selectedTemplate) return;

    // Send API request to Flask backend to generate phishing link
    fetch("/api/host-template", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ template: selectedTemplate })
    })
    .then(response => response.json())
    .then(data => {
        if (data.link) {
            document.getElementById("hostedTemplateLink").innerHTML = `
                <p>Template Hosted at: <a href="${data.link}" target="_blank">${data.link}</a></p>
                <button onclick="copyToClipboard('${data.link}')">Copy Link</button>
            `;
        } else {
            alert("Error: " + data.error);
            document.getElementById("hostedTemplateLink").innerHTML = "";
        }
    })
    .catch(error => {
        console.error("Error hosting template:", error);
        alert("Failed to host template. Please try again.");
    });
});

// Function to copy template link to clipboard
function copyToClipboard(link) {
    navigator.clipboard.writeText(link)
    .then(() => {
        alert("Link copied to clipboard!");
    })
    .catch(error => {
        console.error("Error copying link:", error);
        alert("Failed to copy link. Please try manually.");
    });
}