#include <ESP8266WiFi.h>
#include <DHT.h>
#include <SoftwareSerial.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "trifouille";
const char* password = "commesicommesa";

#define DHTPIN D2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);


// LED pins
#define LED_RED D5
#define LED_GREEN D6
#define LED_BLUE D7

WiFiClient wifiClient;
const char* serverURL = "http://192.168.145.178:8000/save-data/";  
ESP8266WebServer server(80); 

void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);
  
  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_BLUE, LOW);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Define API endpoints for controlling LEDs
  server.on("/control-led", HTTP_POST, handleLEDControl);
  
  // Simple GET request handler
  server.on("/", HTTP_GET, []() {
      server.send(200, "text/plain", "ESP8266 Server is running");
  });

  server.begin();
  Serial.println("HTTP server started");
}

void handleLEDControl() {
    if (server.hasArg("red")) {
        digitalWrite(LED_RED, server.arg("red") == "on" ? HIGH : LOW);
    }
    if (server.hasArg("green")) {
        digitalWrite(LED_GREEN, server.arg("green") == "on" ? HIGH : LOW);
    }
    if (server.hasArg("blue")) {
        digitalWrite(LED_BLUE, server.arg("blue") == "on" ? HIGH : LOW);
    }

    server.send(200, "application/json", "{\"status\":\"success\"}");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Failed to read from DHT sensor!");
      delay(1000);
      return;
    }

    String jsonData = "{\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + "}";

    HTTPClient http;
    http.begin(wifiClient, serverURL);  // Use the updated version with WiFiClient

    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Server Response: " + response);
    } else {
      Serial.println("Error sending data to server");
    }

    http.end();

  }
  server.handleClient();
  delay(1000);  
}