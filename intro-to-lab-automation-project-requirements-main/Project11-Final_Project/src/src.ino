/*
  Project 11 - Final Project
  This sketch reads an accelerometer sensor (simulated via analog input A0),
  maps the sensor reading to an angle (0–180°) for a servo motor,
  displays the angle, buzzer state, and fan state on an OLED display,
  and turns on a buzzer if the angle exceeds a set threshold.
  It also logs the time (ms since start), angle, buzzer state, and fan state via Serial (CSV format).
  Additionally, the fan is controlled by the accelerometer reading: it turns ON when the angle exceeds 90°.
*/

#include <Servo.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// OLED display settings
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1   // Use -1 if sharing the Arduino reset pin
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Hardware pins
const int servoPin = 7;          // Servo motor control pin
const int buzzerPin = 5;         // Buzzer output pin
const int accelerometerPin = A0; // Simulated accelerometer input
const int FAN_PIN = 3;           // Fan control pin

// Thresholds (in degrees)
const int buzzerThresholdAngle = 45;
const int fanThresholdAngle = 90;

// Create a servo object
Servo servoMotor;

// Variable to mark the start time
unsigned long startTime;

void setup() {
  Serial.begin(9600);
  
  // Initialize the servo motor
  servoMotor.attach(servoPin);
  
  // Set buzzer pin as output and ensure it's off
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);

  // Initialize fan control pin as output and ensure it's off
  pinMode(FAN_PIN, OUTPUT);
  digitalWrite(FAN_PIN, LOW);
  
  // Initialize the OLED display
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println(F("SSD1306 allocation failed"));
    while (true); // Halt if display not found
  }
  display.clearDisplay();
  display.display();
  
  // Record the start time
  startTime = millis();
}

void loop() {
  // --- Read the accelerometer sensor ---
  int sensorValue = analogRead(accelerometerPin);
  // Map the analog value (0–1023) to an angle (0–180°)
  int angle = map(sensorValue, 0, 1023, 0, 180);
  
  // --- Update the servo motor ---
  servoMotor.write(angle);
  
  // --- Determine the buzzer state ---
  int buzzerState = 0;
  if (angle > buzzerThresholdAngle) {
    digitalWrite(buzzerPin, HIGH);
    tone(buzzerPin, 120); // Play a tone (120 Hz)
    buzzerState = 1;
  } else {
    digitalWrite(buzzerPin, LOW);
    noTone(buzzerPin);
    buzzerState = 0;
  }
  
  // --- Control the fan based on the accelerometer reading ---
  int fanState = 0;
  if (angle > fanThresholdAngle) {
    digitalWrite(FAN_PIN, HIGH);
    fanState = 1;
  } else {
    digitalWrite(FAN_PIN, LOW);
    fanState = 0;
  }
  
  // --- Update the OLED display ---
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.print("Angle:");
  display.println(angle);
  
  display.print("Buz:");
  if (buzzerState == 1)
    display.println("ON");
  else
    display.println("OFF");
    
  display.print("Fan:");
  if (fanState == 1)
    display.println("ON");
  else
    display.println("OFF");
    
  display.display();
  
  // --- Log data via Serial in CSV format ---
  // Format: [Time_since_start (ms)],[Angle],[BuzzerState],[FanState]
  unsigned long currentTime = millis() - startTime;
  Serial.print(currentTime);
  Serial.print(",");
  Serial.print(angle);
  Serial.print(",");
  Serial.print(buzzerState);
  Serial.print(",");
  Serial.println(fanState);
  
  delay(100); // Wait 100 ms before the next loop iteration
}
