#define BUTTON_PIN 6      // Button connected to pin 6
#define LED_PIN 4         // LED connected to pin 4
#define INTERRUPT_PIN 2   // Interrupt pin (must be 2 or 3 on most Arduinos)

volatile bool buttonPressed = false;  // Flag for button press

void buttonISR() {
    buttonPressed = true;  // Set flag when interrupt occurs
}

void setup() {
    pinMode(BUTTON_PIN, INPUT_PULLUP);  // Enable internal pull-up resistor
    pinMode(LED_PIN, OUTPUT);           // Set LED pin as output
    pinMode(INTERRUPT_PIN, INPUT_PULLUP); // Interrupt pin (connected to button)

    attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), buttonISR, FALLING);  
    // Interrupt triggers when button is pressed

    digitalWrite(LED_PIN, HIGH);  // LED is always ON
    Serial.begin(9600);           // Start serial communication
}

void loop() {
    if (buttonPressed) {
        digitalWrite(LED_PIN, LOW);  // Turn LED OFF when button is pressed
        delay(1000);  // Small delay to debounce 
        digitalWrite(LED_PIN, HIGH); // Turn LED back ON
        buttonPressed = false;  // Reset flag
        Serial.println("Button was pressed!");
    }
}
