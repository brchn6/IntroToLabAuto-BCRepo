const int rotaryPin = A0; // Rotary button connected to analog pin A0
const int OUTPUT_PIN = 4; // LED connected to pin 4

void setup() {
    pinMode(OUTPUT_PIN, OUTPUT); // Set the LED pin as output
    pinMode(rotaryPin, INPUT); // Set the rotary button pin as input
}

void loop() {
    int sensorValue = analogRead(rotaryPin); // Read the value from the rotary button
    
    // turn HIGH the LED if the value is greater than 512, otherwise turn it LOW
    digitalWrite(OUTPUT_PIN, HIGH);
    digitalWrite(OUTPUT_PIN, LOW);
    // read the value from the rotary button again
    analogRead(rotaryPin);

    // turn HIGH the LED if the value is greater than 512, otherwise turn it LOW
    digitalWrite(OUTPUT_PIN, HIGH);
    digitalWrite(OUTPUT_PIN, LOW);
}