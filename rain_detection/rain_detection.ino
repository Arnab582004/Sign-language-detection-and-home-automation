#define BLYNK_TEMPLATE_ID "TMPL3Tn8WWIdN"
#define BLYNK_TEMPLATE_NAME "Rain Alert Notification"
#define BLYNK_AUTH_TOKEN "Rhq8_fiOJH-Sijqrs8wRi60ICmsXtwDF"

#define BLYNK_PRINT Serial

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

#define RAIN_SENSOR_PIN A0
#define RAIN_SENSOR_THRESHOLD 500 

char ssid[] = "Samsung galaxy a73s 5g";
char pass[] = "1234567890";

void setup()
{
  Serial.begin(115200);
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
}

void loop()
{
  int sensorValue = analogRead(RAIN_SENSOR_PIN);
  Serial.print("Rain sensor value: ");
  Serial.println(sensorValue);

  if (sensorValue < RAIN_SENSOR_THRESHOLD) {
    Blynk.logEvent("rainalert");
  }

  Blynk.virtualWrite(V0, sensorValue);

  Blynk.run();
  delay(1000);
}
