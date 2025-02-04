#define OUTPUT_LED_4 4     // LED connected to pin 4

#include <Arduino.h>
#include <MD_PWM.h>        // Include the MD_PWM library

// Initialize PWM object
MD_PWM PWM(4); // PWM on pin 4

void setup() {
    pinMode(OUTPUT_LED_4, OUTPUT); // Set the LED pin as output
    // Initialize PWM on pin 4
    PWM.begin();
}

void loop() {
    for (int i = 0; i <= 255; i++) {
        PWM.write(i);
        delay(10);
    }
    // 3 BLINKS ON 255
    for (int i = 0; i < 3; i++) {
        PWM.write(255);
        delay(500);
        PWM.write(0);
        delay(500);
    }
    for (int i = 255; i >= 0; i--) {
        PWM.write(i);
        delay(10);
    }
}
