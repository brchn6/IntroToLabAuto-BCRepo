#include <Arduino.h>

// Pin definitions
#define LED_PIN 4
#define BUTTON_PIN 2  // Button is connected to pin 2 

// Variables shared between ISR and main loop
volatile bool buttonPressed = true;   // Flag set in the ISR when button is pressed
volatile unsigned long startTime = 0;    // Stores the time when the button was pressed
bool ledOn = false;                      // Tracks whether the LED is currently on

// Interrupt Service Routine for the button press
void buttonISR() {
  // Since we're using INPUT_PULLUP, the button press brings the pin LOW.
  // We trigger on FALLING edge.
  buttonPressed = true; // Set the flag; main loop will handle turning on the LED.
}

void setup() {
  // Initialize the LED pin as output
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);  // Ensure LED is off initially

  // Initialize the button pin as input with internal pull-up enabled
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // Attach interrupt on BUTTON_PIN on the falling edge (button pressed)
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonISR, FALLING);

  // Optionally, start Serial Monitor to see debug messages
  Serial.begin(9600);
}

void loop() {
  // Check if a button press was registered by the ISR
  if (buttonPressed) {
    // Clear the flag, turn on the LED, and record the current time
    buttonPressed = false;
    ledOn = true;
    startTime = millis();
    digitalWrite(LED_PIN, HIGH);
    Serial.println("LED turned ON");
  }

  // If the LED is on, check if 5 seconds have passed
  if (ledOn) {
    if (millis() - startTime >= 5000UL) {  // 5000 milliseconds = 5 seconds
      digitalWrite(LED_PIN, LOW);  // Turn off the LED
      ledOn = false;
      Serial.println("LED turned OFF after 5 seconds");
    }
  }
}
