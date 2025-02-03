// # Project 4: measuring overhead of digitalWrite() with 2 pins

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
const int BUTTEN_PIN_6 = 6; 
const int DELAY_TIME_US = 500000; //corespo=de to 1ms

unsigned long time0;
unsigned long time1;
  
// The setup function runs once when you press reset or power the board
void setup() {
  // Initialize digital pin LED_PIN as an output
  pinMode(LED_PIN_13, OUTPUT);
  pinMode(LED_PIN_12, OUTPUT);
  Serial.begin(9600);
}

// The loop function runs over and over again forever
void loop() {
  Serial.println("setup the pins");
  digitalWrite(LED_PIN_13, HIGH);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_PIN_12, HIGH);   // turn the LED on (HIGH is the voltage level)
  Serial.println("pins are set");
  Serial.println("add calculation");
  time0= micros();
  // add any calculation here
  int a = 1;
  int b = 2;
  int c = a + b;
  int d = c + 1;
  int ff = d + 10000000;
  Serial.println("calculation done");
  time1 = micros();
  Serial.println("time taken for calculation");
  Serial.println(time1-time0);
  digitalWrite(LED_PIN_13, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(LED_PIN_12, LOW);    // turn the LED off by making the voltage LOW
  delayMicroseconds(DELAY_TIME_US); // wait for a second

  // Add interrupt code here
  attachInterrupt(digitalPinToInterrupt(
}

void handleInterrupt() {
  // Interrupt service routine code here
  Serial.println("Interrupt triggered");

}
