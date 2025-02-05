#include <MsTimer2.h>

const int LED_PIN = 13;      // Built-in LED
const int BUTTON_PIN = 2;    // Button pin for interrupt
volatile bool ledState = false;
volatile bool buttonPressed = false;
volatile unsigned long ledDuration = 1000;  // Default duration (ms)

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Configure pins
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  // Attach interrupt for button press
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonISR, FALLING);
}

void loop() {
  // Check for incoming serial data
  if (Serial.available() > 0) {
    // Read the incoming number
    ledDuration = Serial.parseInt();
    
    // Acknowledge receipt
    Serial.print("I received: ");
    Serial.println(ledDuration);
  }

  // Handle button press
  if (buttonPressed) {
    digitalWrite(LED_PIN, HIGH);
    ledState = true;
    MsTimer2::set(ledDuration + 1);  // Set new duration and add 1ms
    MsTimer2::start();  // Start the timer
    Serial.println("1");  // Button and LED on
    buttonPressed = false;  // Reset the flag
  }

  // Report current state
  if (ledState) {
    if (digitalRead(BUTTON_PIN) == LOW) {  // Button still pressed
      Serial.println("1");  // Button and LED on
    } else {
      Serial.println("2");  // Button off, LED still on
    }
  } else {
    Serial.println("0");  // LED off
  }

  delay(100);  // Small delay to prevent serial flooding
}

// Interrupt Service Routine for button press
void buttonISR() {
  if (!ledState) {  // Only trigger if LED is not already on
    buttonPressed = true;
  }
}

// Timer callback function to turn off LED
void turn_off() {
  digitalWrite(LED_PIN, LOW);
  ledState = false;
  MsTimer2::stop();  // Stop the timer
}