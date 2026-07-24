#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  Serial.println("Initializing MPU6050...");
  mpu.initialize();

  // Check connection
  if (mpu.testConnection()) {
    Serial.println("MPU6050 connection successful!");
  } else {
    Serial.println("MPU6050 connection failed!");
    while (1);
  }
}

void loop() {
  int16_t ax, ay, az;
  int16_t gx, gy, gz;

  // Accelerometer aur Gyro values lena
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  Serial.print("aX = "); Serial.print(ax);
  Serial.print(" | aY = "); Serial.print(ay);
  Serial.print(" | aZ = "); Serial.print(az);

  Serial.print(" | gX = "); Serial.print(gx);
  Serial.print(" | gY = "); Serial.print(gy);
  Serial.print(" | gZ = "); Serial.println(gz);

  delay(10000);
}
