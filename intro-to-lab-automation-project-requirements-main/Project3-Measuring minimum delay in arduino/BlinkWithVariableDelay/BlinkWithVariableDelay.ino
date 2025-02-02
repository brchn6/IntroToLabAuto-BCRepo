/**
 * This function reads the temperature from a sensor and returns the value in Celsius.
 * It uses the analogRead function to get the sensor value, then converts it to a voltage,
 * and finally calculates the temperature based on the sensor's characteristics.
 *
 * @return float - The temperature in Celsius.
 */
//set the variable 
const int LED_PIN = 4; // LED connected to digital pin 4 
const int BLINK_TIME = 1; // LED duration of the blink in milliseconds


// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_PIN as an output.
  pinMode(LED_PIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(LED_PIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  delay(BLINK_TIME);                      // wait for a second
  digitalWrite(LED_PIN, LOW);   // turn the LED off by making the voltage LOW
  delay(BLINK_TIME);                      // wait for a second
}