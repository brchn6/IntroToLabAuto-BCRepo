/**
 * This function reads the temperature from a sensor and returns the value in Celsius.
 * It uses the analogRead function to get the sensor value, then converts it to a voltage,
 * and finally calculates the temperature based on the sensor's characteristics.
 *
 * @return float - The temperature in Celsius.
 */
// Set the variable 
const int LED_PIN = 4; // LED connected to digital pin 4 
const int BLINK_TIME = 20; // LED duration of the blink in milliseconds
const int DELAY_TIME_US = 500; // 500 microseconds



// The setup function runs once when you press reset or power the board
void setup() {
  // Initialize digital pin LED_PIN as an output
  pinMode(LED_PIN, OUTPUT);
}

// The loop function runs over and over again forever
void loop() {
  digitalWrite(LED_PIN, HIGH);  // Turn the LED on (HIGH is the voltage level)
  // delay(BLINK_TIME);  // Wait for the specified duration
  delayMicroseconds(DELAY_TIME_US);

  digitalWrite(LED_PIN, LOW);   // Turn the LED off by making the voltage LOW
  // delay(BLINK_TIME);  // Wait for the specified duration
  delayMicroseconds(DELAY_TIME_US);

  
}
