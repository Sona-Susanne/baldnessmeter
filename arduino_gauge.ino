/*
 * Baldness-O-Meter Arduino Servo Gauge
 * =====================================
 * Reads serial input (0-100) over Serial (9600 baud),
 * flashes an LED on Pin 8, and maps the score to servo movement
 * on Pin 9 (0 to 180 degrees).
 */

#include <Servo.h>

// Pin Definitions
const int LED_PIN = 8;
const int SERVO_PIN = 9;

Servo gaugeServo;
int currentScore = 0;

void setup() {
  // Initialize Serial communication at 9600 baud
  Serial.begin(9600);
  
  // Initialize LED pin as output
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Attach servo to Pin 9
  gaugeServo.attach(SERVO_PIN);
  
  // Set initial gauge position (0 degrees = 0% baldness)
  gaugeServo.write(0);
  
  // Startup LED flash test
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(100);
    digitalWrite(LED_PIN, LOW);
    delay(100);
  }
}

void loop() {
  // Check if serial data is available
  if (Serial.available() > 0) {
    // Read integer from serial stream
    int score = Serial.parseInt();
    
    // Validate and constrain score to range 0-100
    score = constrain(score, 0, 100);
    currentScore = score;

    // Map score (0 - 100) to Servo angle (0 - 180 degrees)
    int angle = map(currentScore, 0, 100, 0, 180);
    
    // Move servo to target angle
    gaugeServo.write(angle);

    // Flash LED on Pin 8 to signal update received
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    
    // Debug output back to serial monitor if connected
    Serial.print("Received score: ");
    Serial.print(currentScore);
    Serial.print(" -> Servo Angle: ");
    Serial.println(angle);
  }
}
