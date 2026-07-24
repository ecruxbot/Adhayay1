#include <Servo.h>

Servo myservo;

void setup() {
  myservo.attach(9); // Servo D9 par laga hai
}

void loop() {
  myservo.write(0);   // 0 degree
  delay(1000);
  myservo.write(45);  // 45 degree
  delay(1000);
  myservo.write(90);  // 90 degree
  delay(1000);
  myservo.write(135); // 135 degree
  delay(1000);
  myservo.write(180); // 180 degree
  delay(1000);
}
