#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>

const char* ssid = "realme 8i";
const char* password = "20022002";
const char* django_server = "http://192.168.37.62:8000/fire-alert/";
const char* fire_monitor_server = "http://192.168.37.62:8000/fire_monitor/update/";


WebServer server(80);

// Device GPIO Assignments
#define DEVICE_1 2  // Bulb  
#define DEVICE_2 4  // Fan   
#define DEVICE_3 5  // AC    
#define DEVICE_4 18 // Motor 
#define DEVICE_5 19 // TV    
#define FIRE_SENSOR 21  // Fire sensor GPIO pin

bool lastFireStatus = false;

// HTML for Web Control
const char HTML_PAGE[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 Device Control</title>
</head>
<body>
    <h2>ESP32 Device Control</h2>
    <button onclick="controlDevice('on', '1')">Turn ON Bulb</button>
    <button onclick="controlDevice('off', '1')">Turn OFF Bulb</button><br><br>

    <button onclick="controlDevice('on', '2')">Turn ON Fan</button>
    <button onclick="controlDevice('off', '2')">Turn OFF Fan</button><br><br>

    <button onclick="controlDevice('on', '3')">Turn ON AC</button>
    <button onclick="controlDevice('off', '3')">Turn OFF AC</button><br><br>

    <button onclick="controlDevice('on', '4')">Turn ON Motor</button>
    <button onclick="controlDevice('off', '4')">Turn OFF Motor</button><br><br>

    <button onclick="controlDevice('on', '5')">Turn ON TV</button>
    <button onclick="controlDevice('off', '5')">Turn OFF TV</button><br><br>

    <hr>
    <button onclick="controlDevice('on', 'all')">🔆 Turn ON All Devices</button>
    <button onclick="controlDevice('off', 'all')">🌑 Turn OFF All Devices</button><br><br>

    <script>
        function controlDevice(action, device) {
            fetch(`/device/${action}/${device}/`)
                .then(response => response.text())
                .then(data => alert(data))
                .catch(error => console.error(error));
        }
    </script>
</body>
</html>
)rawliteral";

// Function to send fire alert to Django server
void sendFireAlert() {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(django_server);
        http.addHeader("Content-Type", "application/json");
        int httpResponseCode = http.POST("{\"fire\": \"detected\"}");
        Serial.printf("Fire Alert Sent! Response Code: %d\n", httpResponseCode);
        http.end();
    }
}

// Function to update fire status on Django server
void updateFireStatus(bool status) {
    if (lastFireStatus == status) return;
    lastFireStatus = status;

    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(String(fire_monitor_server) + "?status=" + (status ? "true" : "false"));
        int httpResponseCode = http.GET();
        Serial.printf("Fire Monitor Updated! Response Code: %d\n", httpResponseCode);
        http.end();
    }
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    pinMode(DEVICE_1, OUTPUT);
    pinMode(DEVICE_2, OUTPUT);
    pinMode(DEVICE_3, OUTPUT);
    pinMode(DEVICE_4, OUTPUT);
    pinMode(DEVICE_5, OUTPUT);
    pinMode(FIRE_SENSOR, INPUT);

    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");

    int attempts = 20;
    while (WiFi.status() != WL_CONNECTED && attempts > 0) {
        delay(500);
        Serial.print(".");
        attempts--;
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\nWiFi Connected!");
        Serial.print("ESP32 IP Address: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println("\nFailed to connect! Restarting...");
        ESP.restart();
    }

    server.on("/", []() { server.send(200, "text/html", HTML_PAGE); });

    // Individual Device Control
    server.on("/device/on/1/", []() { digitalWrite(DEVICE_1, HIGH); server.send(200, "text/plain", "Bulb Turned ON"); });
    server.on("/device/off/1/", []() { digitalWrite(DEVICE_1, LOW); server.send(200, "text/plain", "Bulb Turned OFF"); });

    server.on("/device/on/2/", []() { digitalWrite(DEVICE_2, HIGH); server.send(200, "text/plain", "Fan Turned ON"); });
    server.on("/device/off/2/", []() { digitalWrite(DEVICE_2, LOW); server.send(200, "text/plain", "Fan Turned OFF"); });

    server.on("/device/on/3/", []() { digitalWrite(DEVICE_3, HIGH); server.send(200, "text/plain", "AC Turned ON"); });
    server.on("/device/off/3/", []() { digitalWrite(DEVICE_3, LOW); server.send(200, "text/plain", "AC Turned OFF"); });

    server.on("/device/on/4/", []() { digitalWrite(DEVICE_4, HIGH); server.send(200, "text/plain", "Motor Turned ON"); });
    server.on("/device/off/4/", []() { digitalWrite(DEVICE_4, LOW); server.send(200, "text/plain", "Motor Turned OFF"); });

    server.on("/device/on/5/", []() { digitalWrite(DEVICE_5, HIGH); server.send(200, "text/plain", "TV Turned ON"); });
    server.on("/device/off/5/", []() { digitalWrite(DEVICE_5, LOW); server.send(200, "text/plain", "TV Turned OFF"); });

    // Turn ALL Devices ON
    server.on("/device/on/all/", []() { 
        digitalWrite(DEVICE_1, HIGH);
        digitalWrite(DEVICE_2, HIGH);
        digitalWrite(DEVICE_3, HIGH);
        digitalWrite(DEVICE_4, HIGH);
        digitalWrite(DEVICE_5, HIGH);
        server.send(200, "text/plain", "All Devices Turned ON");
    });

    // Turn ALL Devices OFF
    server.on("/device/off/all/", []() { 
        digitalWrite(DEVICE_1, LOW);
        digitalWrite(DEVICE_2, LOW);
        digitalWrite(DEVICE_3, LOW);
        digitalWrite(DEVICE_4, LOW);
        digitalWrite(DEVICE_5, LOW);
        server.send(200, "text/plain", "All Devices Turned OFF");
    });

    server.begin();
    Serial.println("Web server started.");
}

void loop() {
    server.handleClient();

    int fireValue = digitalRead(FIRE_SENSOR);
    if (fireValue == 0) {
        sendFireAlert();
        updateFireStatus(true);
    } else {
        updateFireStatus(false);
    }

    delay(1000);
}
