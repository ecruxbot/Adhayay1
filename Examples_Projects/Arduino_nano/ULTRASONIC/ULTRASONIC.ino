#define TRIG_PIN 4   
#define ECHO_PIN A3 

long duration;
int distance;

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  Serial.begin(9600);
  Serial.println("Ultrasonic Sensor Test");
}

void loop() {
  // Trigger pulse bhejna
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Echo se duration lena
  duration = pulseIn(ECHO_PIN, HIGH);

  // Distance calculate karna (cm me)
  distance = duration * 0.034 / 2;

  // Serial pe print
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(500);
}
