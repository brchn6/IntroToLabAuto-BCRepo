#include <Arduino.h>

// Pin definitions
#define LED_PIN 4
#define BUTTON_PIN 2  // Button is connected to pin 2 

// Variables shared between ISR and main loop
volatile bool buttonPressed = true;   // Flag set in the ISR when button is pressed
volatile unsigned long startTime = 0;    // Stores the time when the button was pressed
bool ledOn = false;                      // Tracks whether the LED is currently on


void buttonISR() {
  // Check if a button press was registered by the ISR
  if (buttonPressed) {
    buttonPressed = false; // If the LED is off, turn it on and start the timer
    ledOn = true;
    startTime = millis();
    digitalWrite(LED_PIN, HIGH);
    Serial.println("LED turned ON");}
}

void setup() {
  // Initialize the LED pin as output
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);  // Ensure LED is off initially

  // Initialize the button pin as input with internal pull-up enabled
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // Attach interrupt on BUTTON_PIN on the falling edge (button pressed)
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonISR, CHANGE);

  // Optionally, start Serial Monitor to see debug messages
  Serial.begin(9600);
}

void loop() {
  // If the LED is on, check if 5 seconds have passed
  if (ledOn) {
    if (millis() - startTime >= 5000UL) {  // 5000 milliseconds = 5 seconds
      digitalWrite(LED_PIN, LOW);  // Turn off the LED
      ledOn = false;
      Serial.println("LED turned OFF after 5 seconds");
    }
  }
}
