#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.begin(9600);
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }

  display.clearDisplay();

  String line1 = "WELCOME";
  String line2 = "TO";
  String line3 = "ECRUXBOT";


  display.setTextSize(1);  
  display.setTextColor(SSD1306_WHITE);

  
  int16_t x1, y1, x2, y2, x3, y3;
  uint16_t w1, h1, w2, h2, w3, h3;

  display.getTextBounds(line1, 0, 0, &x1, &y1, &w1, &h1);
  display.getTextBounds(line2, 0, 0, &x2, &y2, &w2, &h2);
  display.getTextBounds(line3, 0, 0, &x3, &y3, &w3, &h3);

  int gap = 4;  
  int totalHeight = h1 + h2 + h3 + (2 * gap);

  int startY = (SCREEN_HEIGHT - totalHeight) / 2;

  int xLine1 = (SCREEN_WIDTH - w1) / 2;
  int yLine1 = startY + h1;

  int xLine2 = (SCREEN_WIDTH - w2) / 2;
  int yLine2 = yLine1 + gap + h2;

  int xLine3 = (SCREEN_WIDTH - w3) / 2;
  int yLine3 = yLine2 + gap + h3;


  display.setCursor(xLine1, yLine1);
  display.println(line1);

  display.setCursor(xLine2, yLine2);
  display.println(line2);

  display.setCursor(xLine3, yLine3);
  display.println(line3);

  display.display();
}

void loop() {
}
