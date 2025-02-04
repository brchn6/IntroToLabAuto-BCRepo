#define OUTPUT_LED_4 4          // LED connected to pin 4
#define POTENTIOMETER_PIN A0    // Potentiometer connected to analog pin A0
#define INTERRUPT_PIN 2         // Interrupt pin connected to pin 2
#define BUTTON_PIN 6            // Button connected to pin 6

#include <Arduino.h>
#include <MD_PWM.h>             // Include the MD_PWM library

// Initialize PWM object
MD_PWM PWM(OUTPUT_LED_4);       // PWM on pin 4

volatile bool blinkMode = false; // Flag to toggle blinking mode

// Interrupt Service Routine (ISR) for the button press
void handleButtonPress() {
    blinkMode = !blinkMode;     // Toggle the blinking mode
}

void setup() {
    pinMode(OUTPUT_LED_4, OUTPUT);         // Set the LED pin as output
    pinMode(POTENTIOMETER_PIN, INPUT);     // Set potentiometer pin as input
    pinMode(BUTTON_PIN, INPUT_PULLUP);     // Button pin with internal pull-up resistor
    pinMode(INTERRUPT_PIN, INPUT);         // Interrupt pin as input

    attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), handleButtonPress, FALLING); // Trigger interrupt on falling edge

    PWM.begin();                            // Initialize PWM on pin 4
}

void loop() {
    int potValue = analogRead(POTENTIOMETER_PIN);             // Read potentiometer value (0-1023)
    int pwmValue = map(potValue, 0, 1023, 0, 255);            // Map value to PWM range (0-255)

    if (blinkMode) {
        // Blinking mode with dimmer control
        PWM.write(pwmValue);   // LED ON with dimmed value
        delay(500);
        PWM.write(0);          // LED OFF
        delay(500);
    } else {
        // Normal dimmer mode
        PWM.write(pwmValue);   // Adjust LED brightness based on potentiometer
        delay(10);
    }
}