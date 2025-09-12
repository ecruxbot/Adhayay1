#include <IRremote.h>

#define IR_RECEIVE_PIN 2   // TSOP output pin connected to D2

void setup() {
  Serial.begin(9600);
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK); 
  Serial.println("TSOP IR Receiver Ready (IRremote v4.x)");
}

void loop() {
  if (IrReceiver.decode()) {
    Serial.print("IR Code Received: ");
    Serial.println(IrReceiver.decodedIRData.decodedRawData, HEX);

    // Resume receiver for next signal
    IrReceiver.resume();
  }
}
