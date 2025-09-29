#define LED_PIN 7
const bool ACTIVE_LOW = true;

inline void ledOn()  { digitalWrite(LED_PIN, ACTIVE_LOW ? LOW  : HIGH); }
inline void ledOff() { digitalWrite(LED_PIN, ACTIVE_LOW ? HIGH : LOW ); }

void setup() {
  pinMode(LED_PIN, OUTPUT);
  ledOff();                 
}

void loop() {
  ledOn();
  delay(1000);

  for (int i = 0; i < 5; i++) {
    ledOn();
    delay(150);
    ledOff();
    delay(150);
  }
  ledOff();
  while (1) { }        
}
