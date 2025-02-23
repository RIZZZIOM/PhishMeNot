document.addEventListener("DOMContentLoaded", function () {
    // Load SMTP settings (User settings take priority)
    fetch("/api/smtp-settings")
        .then(response => response.json())
        .then(data => {
            document.getElementById("smtpServer").value = data.server || "smtp.gmail.com";
            document.getElementById("smtpPort").value = data.port || "587";
            document.getElementById("smtpEncryption").value = data.encryption || "TLS";
        })
        .catch(error => console.error("Error loading SMTP settings:", error));

    // Load Port Forwarding settings (User settings take priority)
    fetch("/api/port-forwarding-settings")
        .then(response => response.json())
        .then(data => {
            document.getElementById("portForwardingEnabled").checked = data.enabled || false;
            document.getElementById("portForwardingService").value = data.service || "ngrok";
            document.getElementById("portForwardingUrl").value = data.url || "";
        })
        .catch(error => console.error("Error loading Port Forwarding settings:", error));
});

// Save new settings when "Save Changes" button is clicked
document.getElementById("saveSettings").addEventListener("click", function () {
    // Collect values from settings form
    const smtpServer = document.getElementById("smtpServer").value;
    const smtpPort = document.getElementById("smtpPort").value;
    const smtpUsername = document.getElementById("smtpUsername") ? document.getElementById("smtpUsername").value : "";
    const smtpPassword = document.getElementById("smtpPassword") ? document.getElementById("smtpPassword").value : "";
    const smtpEncryption = document.getElementById("smtpEncryption").value;

    const portForwardingEnabled = document.getElementById("portForwardingEnabled").checked;
    const portForwardingService = document.getElementById("portForwardingService").value;
    const portForwardingUrl = document.getElementById("portForwardingUrl").value;

    const enableMasking = document.getElementById("enableMasking") ? document.getElementById("enableMasking").checked : false;
    const maskingDomain = document.getElementById("maskingDomain") ? document.getElementById("maskingDomain").value : "";

    // Log values for debugging
    console.log("SMTP Settings:", { smtpServer, smtpPort, smtpUsername, smtpPassword, smtpEncryption });
    console.log("Port Forwarding:", { portForwardingEnabled, portForwardingService, portForwardingUrl });
    console.log("Email Masking:", { enableMasking, maskingDomain });

    // Construct API request payload
    const updatedSettings = {
        smtp: {
            server: smtpServer,
            port: smtpPort,
            encryption: smtpEncryption
        },
        port_forwarding: {
            enabled: portForwardingEnabled,
            service: portForwardingService,
            url: portForwardingUrl
        }
    };

    // Only add optional values if they exist
    if (smtpUsername) updatedSettings.smtp.username = smtpUsername;
    if (smtpPassword) updatedSettings.smtp.password = smtpPassword;
    if (enableMasking !== undefined) updatedSettings.email_masking = { enabled: enableMasking, domain: maskingDomain };

    // Send API request to save settings
    fetch("/api/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedSettings)
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error("Error saving settings:", error));
});
