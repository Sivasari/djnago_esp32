document.addEventListener("DOMContentLoaded", function () {
    function checkFireStatus() {
        fetch("/status/") // Calls Django's fire_status view
            .then(response => response.json())
            .then(data => {
                const fireStatusElement = document.getElementById("fire-status");
                const fireNotification = document.getElementById("fire-notification");

                if (data.fire_detected) {
                    fireStatusElement.innerHTML = "🔥 Fire Detected!";
                    fireNotification.innerHTML = "WARNING! Fire Detected!";
                    fireNotification.style.display = "block";  // Show alert
                } else {
                    fireStatusElement.innerHTML = "✅ No Fire";
                    fireNotification.style.display = "none"; // Hide alert
                }
            })
            .catch(error => console.error("Error fetching fire status:", error));
    }

    setInterval(checkFireStatus, 5000); // Fetch fire status every 5 seconds
    checkFireStatus(); // Run immediately on page load
});
