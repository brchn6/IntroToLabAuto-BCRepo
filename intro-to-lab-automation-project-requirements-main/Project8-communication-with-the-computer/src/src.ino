
# include <Arduino.h>
#include <MsTimer2.h>


// Define the pin for the LED and the button
# define LED_PIN_4 4
# define BUTTON_PIN 2

// Variable to store the received number
unsigned long receivedTime = 0;

// Function to turn off the LED
void turn_off() {
  digitalWrite(LED_PIN_4, LOW);
  MsTimer2::stop();
}

// Interrupt service routine for the button press
void buttonPressed() {
  if (receivedTime > 0) {
    digitalWrite(LED_PIN_4, HIGH);
    MsTimer2::set(receivedTime , turn_off); // Set the timer
    MsTimer2::start();
  }
}

void setup() {
  // Initialize the serial communication
  Serial.begin(9600);

  // Initialize the LED and button pins
  pinMode(LED_PIN_4, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // Attach the interrupt to the button pin
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonPressed, FALLING);

  // Print a startup message
  Serial.println("Arduino is ready to receive data.");
}

void loop() {
  // Check if data is available on the serial port
  if (Serial.available() > 0) {
    // Read the incoming data
    String input = Serial.readStringUntil('\n');
    receivedTime = input.toInt();

    // Print the received number
    Serial.print("I received: ");
    Serial.println(receivedTime);
  }
}
