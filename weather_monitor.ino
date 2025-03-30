#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BMP280 bmp; 

float temperature, pressure, altitude;


const char* ssid = "Samsung galaxy a73s 5g"; 
const char* password = "1234567890"; 

WiFiServer server(80);

void setup() {
Serial.begin(115200);
if (!bmp.begin(0x76)) {
Serial.println("Could not find a valid BMP280 sensor, check wiring!");
while (1);
}

Serial.println("Connecting to Wi-Fi");
WiFi.begin(ssid, password);

while (WiFi.status() != WL_CONNECTED) {
delay(1000);
Serial.print(".");
}

Serial.println("\nWiFi connected");
Serial.print("IP Address: ");
Serial.println(WiFi.localIP());

server.begin();
}

void loop() {
WiFiClient client = server.available();
if (client) {
String request = client.readStringUntil('\r');
client.flush();

temperature = bmp.readTemperature();
pressure = bmp.readPressure() / 100.0F;
altitude = bmp.readAltitude(SEALEVELPRESSURE_HPA);

String html = SendHTML(temperature, pressure, altitude);

client.println("HTTP/1.1 200 OK");
client.println("Content-type:text/html");
client.println();
client.println(html);
client.println();
delay(1);
client.stop();
}
}

String SendHTML(float temperature, float pressure, float altitude) {
String ptr = "<!DOCTYPE html>";
ptr += "<html>";
ptr += "<head>";
ptr += "<title>Smart Weather Monitoring with ESP32 and BMP280 Web Server</title>";
ptr += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>";
ptr += "<style>";
ptr += "body { font-family: Arial, sans-serif; margin: 0; padding: 0; text-align: center; background-color: #f4f4f4; color: #333; }";
ptr += "h1 { font-size: 2.5em; margin: 20px 0; }";
ptr += ".data { margin: 20px auto; padding: 20px; background: #fff; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); width: 90%; max-width: 400px; }";
ptr += ".icon { width: 50px; margin: 0 auto 10px; }";
ptr += ".label { font-size: 1.2em; font-weight: bold; }";
ptr += ".value { font-size: 2em; color: #007BFF; }";
ptr += "</style>";
ptr += "</head>";
ptr += "<body>";
ptr += "<h1>ESP32 Weather Station</h1>";

ptr += "<div class='data'>";
ptr += "<img src='https://img.icons8.com/ios-filled/50/temperature.png' alt='Temperature Icon' class='icon'>";
ptr += "<div class='label'>Temperature</div>";
ptr += "<div class='value'>" + String(temperature, 1) + " &deg;C</div>";
ptr += "</div>";

ptr += "<div class='data'>";
ptr += "<img src='https://img.icons8.com/ios-filled/50/pressure.png' alt='Pressure Icon' class='icon'>";
ptr += "<div class='label'>Pressure</div>";
ptr += "<div class='value'>" + String(pressure, 1) + " hPa</div>";
ptr += "</div>";

ptr += "<div class='data'>";
ptr += "<img src='https://img.icons8.com/ios-filled/50/mountain.png' alt='Altitude Icon' class='icon'>";
ptr += "<div class='label'>Altitude</div>";
ptr += "<div class='value'>" + String(altitude, 1) + " m</div>";
ptr += "</div>";

ptr += "</body>";
ptr += "</html>";

return ptr;
}
