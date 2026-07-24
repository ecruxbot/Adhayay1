int switchPin = 8;    // switch connected to D8
int switchState = 0;  

void setup() {
  pinMode(switchPin, INPUT_PULLUP);  
  Serial.begin(9600);
  Serial.println("Switch Test Start");
}

void loop() {
  switchState = digitalRead(switchPin);

  if (switchState == LOW) {   // button pressed
    Serial.println("Switch Pressed");
  } else {                    // button released
    Serial.println("Switch Released");
  }

  delay(200);
}
