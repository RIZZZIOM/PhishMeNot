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

            data.forEach(entry => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${entry.campaign_name}</td>
                    <td>${entry.timestamp}</td>
                    <td>${entry.sender_email}</td>
                    <td>${entry.target_email}</td>
                    <td>${entry.username}</td>
                    <td>${entry.password}</td>
                `;

                table.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching campaign results:", error));
}
