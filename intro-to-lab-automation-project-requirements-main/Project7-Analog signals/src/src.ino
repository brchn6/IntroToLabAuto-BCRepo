const int rotaryPin = A0; // Rotary button connected to analog pin A0

void setup() {
    Serial.begin(9600); // Start serial communication for debugging
}

void loop() {
    int sensorValue = analogRead(rotaryPin); // Read the value from the rotary button
    Serial.print("Sensor Value: ");
    Serial.print(sensorValue);
    Serial.print("\n");
    delay(100); // Small delay for stability
}