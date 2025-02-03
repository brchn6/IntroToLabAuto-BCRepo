/**
 * This function reads the temperature from a sensor and returns the value in Celsius.
 * It uses the analogRead function to get the sensor value, then converts it to a voltage,
 * and finally calculates the temperature based on the sensor's characteristics.
 *
 * @return float - The temperature in Celsius.
 *  # Project 5 - Reacting to input part I: Interrupts
 * 
 * 1. Make led light on button press
 * 2. Learn how to debug code by establish communication with the computer using the Serial library
 * 3. Understand the difference between polling and interrupt and benefits of using interrupts over polling
 * 4. Learn how to use interrupts in Arduino
 * 
 * ## Light led on button press (arduino code)
 *  - button pin is 6, grove led pin is 4
 *  - read value from button pin. If button is pressed (how can you tell?) turn grove led on. If button is not pressed, turn it off
 *  - test that this works.
 * 
 * ## Simulate additional long process
 * - Add a delay(1000) to your loop. The purpose of this delay is to simulate an additional long process in your system, such as data acquisition, a long measurement, etc.
 * - add Serial statements before and after the delay
 * - test if lighting led still works. Why or why not?
 * answer here: __________
 * 
 * ## Use interrupt to light led
 * - Add code to create an interrupt pin (why can't it be the button pin?). Use a variable for this.
 * - Short the interrupt pin with the button pin
 * - test. Does it work?
 * 
 * ## Exercises
 *  - commit and upload your code in this project folder.
 * 
 * 
    */

#include <Arduino.h>

const int LED_PIN = 4;      // LED connected to digital pin 4
const int BUTTON_PIN = 6;   // Button connected to digital pin 6
const int DELAY_MS = 1000;  // Delay of 1 second

void setup() {
    pinMode(LED_PIN, OUTPUT);   
    pinMode(BUTTON_PIN, INPUT_PULLUP); 
    Serial.begin(9600); // Start serial communication
}

void loop() {
    int buttonState = digitalRead(BUTTON_PIN); // Read button state

    if (buttonState == HIGH) {
        delay(DELAY_MS); // Simulate long process
        digitalWrite(LED_PIN, HIGH); // Turn on LED
        Serial.println("Button pressed!");
    } else {
        digitalWrite(LED_PIN, LOW); // Turn off LED
        // Serial.println("Button not pressed!");
    }
}
