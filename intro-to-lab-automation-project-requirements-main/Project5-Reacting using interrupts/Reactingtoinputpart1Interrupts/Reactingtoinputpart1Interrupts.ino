#define INTERRUPT_PIN 2   // Interrupt-capable pin (connect button here)
#define LED_PIN 4         // LED connected to pin 4
#define BUTTON 6

volatile int buttonState = LOW;  // Declare buttonState as a global variable

// Interrupt Service Routine
void buttonISR() {
    buttonState = digitalRead(BUTTON);
    digitalWrite(LED_PIN, buttonState);
}   

void setup() {
    pinMode(INTERRUPT_PIN, LOW);  // Enable internal pull-up resistor
    pinMode(LED_PIN, OUTPUT);              // Set LED as output

    attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), buttonISR, CHANGE);  // Trigger on state change

    digitalWrite(LED_PIN, LOW);            // LED starts OFF
    Serial.begin(9600);                    // Start serial communication
}

void loop() {
    Serial.println("Calculating...");
    delay(1000);

    if (digitalRead(INTERRUPT_PIN) == 1) {
        Serial.println("Button is currently pressed.");
    } else {
        Serial.println("Button is currently released.");
    }
}