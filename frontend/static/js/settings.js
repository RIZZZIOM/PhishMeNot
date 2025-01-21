document.getElementById('saveSettings').addEventListener('click', function () {
    // Collect values from settings form
    const smtpServer = document.getElementById('smtpServer').value;
    const smtpPort = document.getElementById('smtpPort').value;
    const smtpUsername = document.getElementById('smtpUsername').value;
    const smtpPassword = document.getElementById('smtpPassword').value;
    const smtpEncryption = document.getElementById('smtpEncryption').value;
    const portForwardingService = document.getElementById('portForwardingService').value;
    const portForwardingUrl = document.getElementById('portForwardingUrl').value;
    const enableMasking = document.getElementById('enableMasking').checked;
    const maskingDomain = document.getElementById('maskingDomain').value;

    // Placeholder logic for saving settings
    console.log('SMTP Server:', smtpServer);
    console.log('SMTP Port:', smtpPort);
    console.log('SMTP Username:', smtpUsername);
    console.log('SMTP Password:', smtpPassword);
    console.log('SMTP Encryption:', smtpEncryption);
    console.log('Port Forwarding Service:', portForwardingService);
    console.log('Port Forwarding URL:', portForwardingUrl);
    console.log('Enable Masking:', enableMasking);
    console.log('Masking Domain:', maskingDomain);

    alert('Settings saved successfully!');
});
