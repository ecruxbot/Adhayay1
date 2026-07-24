char c;

void setup() {
  Serial.begin(9600);   
  Serial.println("Bluetooth Ready!");
}

void loop() {
  if (Serial.available()) {
    c = Serial.read();
    Serial.write(c);   // Jo mila wahi wapas bhej dega
  }
}
