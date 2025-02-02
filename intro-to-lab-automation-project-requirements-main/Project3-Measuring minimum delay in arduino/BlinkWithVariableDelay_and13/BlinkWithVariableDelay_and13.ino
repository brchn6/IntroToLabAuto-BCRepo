/**
 * This function reads the temperature from a sensor and returns the value in Celsius.
 * It uses the analogRead function to get the sensor value, then converts it to a voltage,
 * and finally calculates the temperature based on the sensor's characteristics.
 *
 * @return float - The temperature in Celsius.
 */
// Set the variables
const int LED_PIN_4 = 4;    // LED connected to digital pin 4
const int LED_PIN_13 = 13;  // LED connected to digital pin 13
const int LED_PIN_1 = 1;  //LED connected to digital pin 1
const int BLINK_TIME_13 = 1;   // Blink duration for pin 13 in milliseconds
const int BLINK_TIME_4 = 33;   // Blink duration for pin 4 in milliseconds
const int BLINK_TIME_1 =66; // Blink duration for pin 1 in milliseconds



// The setup function runs once when you press reset or power the board
void setup() {
  // Initialize digital pins as outputs
  pinMode(LED_PIN_4, OUTPUT);
  pinMode(LED_PIN_13, OUTPUT);
  pinMode(LED_PIN_1, OUTPUT);
}

// The loop function runs over and over again forever
void loop() {
  // Blink LED on pin 13
  digitalWrite(LED_PIN_13, HIGH);   // Turn on LED on pin 13
  delay(BLINK_TIME_13);             // Wait for 1 ms
  digitalWrite(LED_PIN_13, LOW);    // Turn off LED on pin 13

  // Blink LED on pin 4
  digitalWrite(LED_PIN_4, HIGH);    // Turn on LED on pin 4
  delay(BLINK_TIME_4);              // Wait for 33 ms
  digitalWrite(LED_PIN_4, LOW);     // Turn off LED on pin 4
  
  // Blink LED on pin 1
  digitalWrite(LED_PIN_1, HIGH);    // Turn on LED on pin 1
  delay(BLINK_TIME_1);              // Wait for 33 ms
  digitalWrite(LED_PIN_1, LOW);     // Turn off LED on pin 1
}
