#include <Adafruit_NeoPixel.h>

#define LED_PIN     6   // WS2812 Data pin
#define LED_COUNT   1   // Sirf ek LED

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

// Function to set color
void setColor(uint8_t r, uint8_t g, uint8_t b) {
  strip.setPixelColor(0, strip.Color(r, g, b));
  strip.show();
}

void setup() {
  strip.begin();
  strip.show();             // Saare LED off
  strip.setBrightness(100); // Brightness 0-255
}

void loop() {
  setColor(255, 0, 0);   // Red
  delay(1000);

  setColor(0, 255, 0);   // Green
  delay(1000);

  setColor(0, 0, 255);   // Blue
  delay(1000);

  setColor(255, 255, 0); // Yellow
  delay(1000);

  setColor(0, 255, 255); // Cyan
  delay(1000);

  setColor(255, 0, 255); // Magenta
  delay(1000);

  setColor(255, 255, 255); // White
  delay(1000);

  setColor(0, 0, 0);     // Off
  delay(1000);
}
