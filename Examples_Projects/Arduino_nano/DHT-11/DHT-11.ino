#include <DHT.h>
#define DHTPIN 2    
#define DHTTYPE DHT11   

DHT dht(DHTPIN, DHTTYPE);
void setup() {
  Serial.begin(9600);
  dht.begin();
  Serial.println("DHT11 Sensor Test");
}

void loop() {
  // Kuch delay dena zaroori hai DHT11 ke liye
  delay(2000);

  float h = dht.readHumidity();       // Humidity read
  float t = dht.readTemperature();    // Temperature read (Celsius)

  // Agar reading fail ho gayi
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Output serial monitor pe
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.println(" °C");
}
