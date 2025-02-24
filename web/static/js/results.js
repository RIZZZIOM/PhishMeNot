document.addEventListener("DOMContentLoaded", function () {
    fetchResultsOverview();
    fetchCampaignResults();
});

// 📌 Fetch total campaigns & credentials captured
function fetchResultsOverview() {
    fetch("/api/results/overview")
        .then(response => response.json())
        .then(data => {
            document.getElementById("totalCampaigns").textContent = data.total_campaigns || 0;
            document.getElementById("totalCredentials").textContent = data.total_credentials || 0;
        })
        .catch(error => console.error("Error fetching results overview:", error));
}

// 📌 Fetch and populate campaign details table
function fetchCampaignResults() {
    fetch("/api/results/campaigns")
        .then(response => response.json())
        .then(data => {
            const table = document.querySelector(".campaign-results table");

            // ✅ Clear previous table content
            table.innerHTML = `
                <thead>
                    <tr>
                        <th>Template Name</th>
                        <th>Timestamp</th>
                        <th>Email Sender</th>
                        <th>Target Email</th>
                        <th>Username</th>
                        <th>Password</th>
                    </tr>
                </thead>
                <tbody></tbody>
            `;

            const tbody = table.querySelector("tbody");

            if (data.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;">No data available</td></tr>`;
                return;
            }

            data.forEach(entry => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${entry.template_name}</td>
                    <td>${entry.timestamp}</td>
                    <td>${entry.sender_email}</td>
                    <td>${entry.target_email}</td>
                    <td>${entry.username}</td>
                    <td>${entry.password}</td>
                `;

                tbody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching campaign results:", error));
}
