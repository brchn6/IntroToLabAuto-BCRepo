/*
  Project 11 - Final Project
  This sketch reads an accelerometer sensor (simulated via analog input A0),
  maps the sensor reading to an angle (0-180°) for a servo motor,
  displays the angle, buzzer state, and fan state on an OLED display,
  and turns on a buzzer if the angle exceeds a set threshold.
  It also logs the time (ms since start), angle, buzzer state, and fan state via Serial (CSV format).
  Additionally, the fan is turned on when a button is pressed.
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
const int FAN_PIN = 3;           // Fan control pin (added semicolon)
const int buttonPin = 2;         // Button input pin

// Threshold for buzzer activation (in degrees)
const int thresholdAngle = 45;

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

  // Initialize button pin as input with internal pull-up resistor
  pinMode(buttonPin, INPUT_PULLUP);
  
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
  // (For this example, we simulate it using analogRead)
  int sensorValue = analogRead(accelerometerPin);
  // Map the analog value (0–1023) to an angle (0–180°)
  int angle = map(sensorValue, 0, 1023, 0, 180);
  
  // --- Update the servo motor ---
  servoMotor.write(angle);
  
  // --- Determine the buzzer state ---
  // Turn the buzzer ON if the angle exceeds the threshold
  int buzzerState = 0;
  if (angle > thresholdAngle) {
    digitalWrite(buzzerPin, HIGH);
    tone(buzzerPin, 120); // Play a 1kHz tone
    buzzerState = 1;
  } else {
    digitalWrite(buzzerPin, LOW);
    noTone(buzzerPin);
    buzzerState = 0;
  }
  
  // --- Check the button to control the fan ---
  // Since the button is set with an internal pull-up,
  // it will read LOW when pressed.
  static bool fanState = false; // Variable to store the fan state
  static bool lastButtonState = HIGH; // Variable to store the last button state

  int buttonState = digitalRead(buttonPin);
  if (buttonState == LOW && lastButtonState == HIGH) {
    // Toggle the fan state when the button is pressed
    fanState = !fanState;
    digitalWrite(FAN_PIN, fanState ? HIGH : LOW);
  }
  lastButtonState = buttonState;

  
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
  if (digitalRead(FAN_PIN) == HIGH)
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
  Serial.println(digitalRead(FAN_PIN) == HIGH ? 1 : 0);
  
  delay(100); // Wait 100 ms before the next loop iteration
}
