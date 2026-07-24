// 5-Channel IR Sensor Reading Code
// Pinout:
// ir1 = A5
// ir2 = A1
// ir3 = A2
// ir4 = A3
// ir5 = A4

#define IR1 A5
#define IR2 A1
#define IR3 A2
#define IR4 A3
#define IR5 A4

void setup() {
  Serial.begin(9600);

  pinMode(IR1, INPUT);
  pinMode(IR2, INPUT);
  pinMode(IR3, INPUT);
  pinMode(IR4, INPUT);
  pinMode(IR5, INPUT);
}

void loop() {
  int s1 = digitalRead(IR1);
  int s2 = digitalRead(IR2);
  int s3 = digitalRead(IR3);
  int s4 = digitalRead(IR4);
  int s5 = digitalRead(IR5);

  // Serial print in 1,0 format
  Serial.print(s1);
  Serial.print(" ");
  Serial.print(s2);
  Serial.print(" ");
  Serial.print(s3);
  Serial.print(" ");
  Serial.print(s4);
  Serial.print(" ");
  Serial.println(s5);

  delay(200);  // थोड़ा stable output के लिए delay
}
