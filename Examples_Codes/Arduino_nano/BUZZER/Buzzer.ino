#define BUZZER_PIN 5

// ---- Optional: few musical note frequencies (Hz) ----
#define NOTE_C4  262
#define NOTE_D4  294
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_G4  392
#define NOTE_A4  440
#define NOTE_B4  494
#define NOTE_C5  523

// ===== Active buzzer helpers (simple ON/OFF) =====
void buzzerOn()  { pinMode(BUZZER_PIN, OUTPUT); digitalWrite(BUZZER_PIN, HIGH); }
void buzzerOff() { digitalWrite(BUZZER_PIN, LOW); }

// Pattern: N beeps with on/off durations (ms)
void beep(int count, int onMs, int offMs) {
  pinMode(BUZZER_PIN, OUTPUT);
  for (int i = 0; i < count; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(onMs);
    digitalWrite(BUZZER_PIN, LOW);
    delay(offMs);
  }
}

// ===== Passive buzzer helpers (tones) =====
// Single tone at freq (Hz) for durMs
void playTone(unsigned int freq, unsigned int durMs) {
  tone(BUZZER_PIN, freq);
  delay(durMs);
  noTone(BUZZER_PIN);
  delay(10);
}

// Sweep siren between f1..f2 (Hz)
void siren(unsigned int f1, unsigned int f2, unsigned int step, unsigned int stepMs, int cycles) {
  for (int c = 0; c < cycles; c++) {
    for (unsigned int f = f1; f <= f2; f += step) { tone(BUZZER_PIN, f); delay(stepMs); }
    for (unsigned int f = f2; f >= f1; f -= step) { tone(BUZZER_PIN, f); delay(stepMs); if (f < step) break; }
  }
  noTone(BUZZER_PIN);
}

// Simple melody (notes + durations)
void melodyDemo() {
  unsigned int notes[] = { NOTE_C4, NOTE_D4, NOTE_E4, NOTE_F4, NOTE_G4, NOTE_A4, NOTE_B4, NOTE_C5 };
  unsigned int dur[]   = { 200,     200,     200,     200,     200,     200,     200,     400   };
  for (int i = 0; i < 8; i++) playTone(notes[i], dur[i]);
}

void setup() {
  // Nothing special needed
}

void loop() {
  // ---- ACTIVE BUZZER DEMOS (on/off) ----
  beep(2, 150, 150);     // Double short beep
  delay(400);
  buzzerOn(); delay(500); buzzerOff(); delay(300);  // Solid beep

  // ---- PASSIVE BUZZER DEMOS (tones) ----
  playTone(1000, 200);   // 1 kHz ping
  playTone(1500, 200);
  playTone(2000, 200);

  siren(600, 1600, 20, 8, 2);  // Woo-woo siren
  melodyDemo();                // Simple scale
  delay(600);
}
