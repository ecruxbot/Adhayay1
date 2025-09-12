int ldrPin = 3;   
int ldrState = 0; 

void setup() {
  pinMode(ldrPin, INPUT);
  Serial.begin(9600);
  Serial.println("Digital LDR Test\n");
}

void loop() {
  ldrState = digitalRead(ldrPin);

  if (ldrState == LOW) {  
    Serial.println("Bright Light Detected");
  } else {
    Serial.println("Darkness Detected");
  }

  delay(500);
}
