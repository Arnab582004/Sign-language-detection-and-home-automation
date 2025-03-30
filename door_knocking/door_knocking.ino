#define BLYNK_TEMPLATE_ID "TMPL3FKp1LQO8"
#define BLYNK_TEMPLATE_NAME "Door Knock Alert"
#define BLYNK_AUTH_TOKEN "cbejqNr1Pkul4zvVStwU69Po9sG-UGs0"

#define BLYNK_PRINT Serial
#include <BlynkSimpleEsp32.h>
 
// Blynk settings
char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = "Samsung galaxy a73s 5g";
char pass[] = "1234567890";

// Vibration sensor settings
const int vibrationPin = 34; // Use the appropriate analog pin on your ESP8266
const int threshold = 500;  // Adjust this threshold based on your sensor and environment

// Blynk Virtual Pins
#define VIRTUAL_PIN_VIBRATION  V1  
// Timer settings
BlynkTimer timer;

// Function prototypes
void checkVibration();
void sendAlert();

void setup() {
  Serial.begin(115200);

  Blynk.begin(auth, ssid, pass);

  timer.setInterval(1000, checkVibration);
}

void loop() {
  Blynk.run();
  timer.run();
}

void checkVibration() {
  int vibrationValue = analogRead(vibrationPin);
   Serial.print("Vibration Value: ");
   Serial.println(vibrationValue);
  Blynk.virtualWrite(VIRTUAL_PIN_VIBRATION, vibrationValue);

  if (vibrationValue > threshold) {
   
    Serial.println("Vibration detected!");
    Blynk.logEvent("door_knocking","Door is knocking by someone");
    
  }
}
