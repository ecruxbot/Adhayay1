int buzzer = A0;

void setup() {
  pinMode(buzzer, OUTPUT);
}

void loop() {
  // Belachav fast vibe
  for (int i = 0; i < 50; i++) {
    tone(buzzer, 500);   // dhol (bass)
    delay(80);
    noTone(buzzer);
    delay(20);

    tone(buzzer, 700);   // tasha (sharp)
    delay(60);
    noTone(buzzer);
    delay(30);

    tone(buzzer, 900);   // fast high note
    delay(40);
    noTone(buzzer);
    delay(10);
  }
}
