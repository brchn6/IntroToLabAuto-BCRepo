#include <Arduino.h>
#include <MsTimer2.h>

// Pin definitions
#define LED_PIN 4
#define BUTTON_PIN 2  // Button is connected to pin 2

// Flags to indicate the state of the LED
volatile bool ledOn = false;

// This is the function name callback 
void turnOffLED() {
  digitalWrite(LED_PIN, LOW);   // Turn off the LED
  ledOn = false;
  MsTimer2::stop();             // Stop the timer so it doesn't call the callback again
  Serial.println("LED turned OFF after 5 s");
}

void buttonISR() {
  // Only act if the LED is not already on
  if (!ledOn) {
    ledOn = true;
    digitalWrite(LED_PIN, HIGH);  // Turn on the LED
    Serial.println("LED turned ON");

    
    MsTimer2::set(5000, turnOffLED);
    MsTimer2::start();
  }
}

void setup() {
  // Initialize LED pin as output and ensure it's initially off
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Initialize the button pin as input with internal pull-up resistor enabled
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonISR, CHANGE);

  // Start Serial Monitor for debugging messages.
  Serial.begin(9600);
}

void loop() {
  delay(1000);
}
