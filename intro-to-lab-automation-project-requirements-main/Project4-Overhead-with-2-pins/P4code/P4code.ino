// # Project 4: measuring overhead of digitalWrite() with 2 pins

// 1. Comparing different types of time overhead

// ## write a program that does the following:
// - copy your code from project 3 to projet 4
// - Blink an LED on pin 13 with delay 1 ms
// - Blink an LED on pin 12 with delay 1 ms, in this case there isn't actually a LED connected to this pin, but we can still use it to measure the overhead of the digitalWrite() function, using the logic analyzer.
// - both leds should be HIGH, then delay, then both leds LOW, then delay
// - connect the pins to two inputs in the logic analyzer and don't forget to add the ground connection from the Arduino to the logic analyzer.

// ## Exercise 1
// - measure the delay between the two digitalWrite() functions using the logic analyzer.
// Paste screenshots below:

// enter the delay in usec here:  __________

// ## write a 2nd program that does the following:
// - based on the first program, add any calculation (adding one to an additional variable for example) and store the result in a variable between the two digitalWrite() functions.

// ## Exercise 2
// - measure the delay the originated from the calculation between the two digitalWrite() functions using the logic analyzer.
// Paste screenshots below:

// enter the delay in usec here:  __________

// ## Exercise 3
// - Use chatGPT or similar to find how to write simultaneously to both pins. Measure the delay between the pins now. 
// - Paste a screenshot below.

// ## Git
//  - Commit and push the two programs and the README into the repository

const int LED_PIN_13 = 13; //this line indacates that the LED is connected to pin 13
const int LED_PIN_12 = 12; 
const int DELAY_TIME_US = 1000; //corespo=de to 1ms
  
// The setup function runs once when you press reset or power the board
void setup() {
  // Initialize digital pin LED_PIN as an output
  pinMode(LED_PIN_13, OUTPUT);
  pinMode(LED_PIN_12, OUTPUT);

}

// The loop function runs over and over again forever
void loop() {
  digitalWrite(LED_PIN_13, HIGH);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_PIN_12, HIGH);   // turn the LED on (HIGH is the voltage level)
  delayMicroseconds(DELAY_TIME_US);               // wait for a second
  digitalWrite(LED_PIN_13, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(LED_PIN_12, LOW);    // turn the LED off by making the voltage LOW
  delayMicroseconds(DELAY_TIME_US);               // wait for a second
}
