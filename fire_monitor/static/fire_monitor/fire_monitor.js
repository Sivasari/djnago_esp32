document.addEventListener("DOMContentLoaded", function () {
    // Alarm sound
    let alarmSound = new Audio("/static/fire_monitor/alarm.mp3"); // Ensure alarm.mp3 is in the static folder

    function checkFireStatus() {
        fetch("/fire_monitor/status/") // This URL should return JSON with fire detection status
            .then(response => response.json())
            .then(data => {
                let statusElement = document.getElementById("fire-status");
                let notificationElement = document.getElementById("fire-notification");

                if (data.fire_detected) {
                    // Update status
                    statusElement.innerText = "🔥 Fire Detected!";
                    statusElement.style.color = "red";

                    // Show notification
                    notificationElement.innerText = "🚨 Fire Alert! Appliances turned off automatically.";
                    notificationElement.style.display = "block";

                    // Play alarm sound
                    alarmSound.play();
                } else {
                    // No fire detected
                    statusElement.innerText = "✅ No Fire";
                    statusElement.style.color = "green";

                    // Hide notification
                    notificationElement.style.display = "none";

                    // Stop alarm if playing
                    alarmSound.pause();
                    alarmSound.currentTime = 0;
                }
            })
            .catch(error => console.error("Error fetching fire status:", error));
    }

    // Call the function every 3 seconds to check for fire
    setInterval(checkFireStatus, 3000);
});
