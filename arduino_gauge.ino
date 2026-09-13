/*
 * Baldness-O-Meter Arduino Servo Gauge
 * =====================================
 * Reads serial input (0-100) over Serial (9600 baud),
 * flashes LED on Pin 8 according to threat tier,
 * maps score to 90° -> 0° inverted servo range on Pin 9,
 * and holds the verdict posture for 5 seconds.
 */

#include <Servo.h>

// Pin Definitions
const int LED_PIN = 8;
const int SERVO_PIN = 9;

Servo gaugeServo;

void setup() {
  // Initialize Serial communication at 9600 baud
  Serial.begin(9600);
  
  // Initialize LED pin as output
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Attach servo to Pin 9
  gaugeServo.attach(SERVO_PIN);
  
  // Set rest position directly to 90 degrees (Vertical / Safe baseline)
  gaugeServo.write(90);
}

void loop() {
  // Check if serial data is available
  if (Serial.available() > 0) {
    // Read integer from serial stream
    int score = Serial.parseInt();
    
    // Constrain score to valid 0-100 range
    score = constrain(score, 0, 100);

    // Strobe LED briefly to signal score receipt
    for (int i = 0; i < 3; i++) {
      digitalWrite(LED_PIN, HIGH);
      delay(50);
      digitalWrite(LED_PIN, LOW);
      delay(50);
    }

    // Map score (0-100) to inverted Servo angle (90° down to 0°)
    int targetAngle = map(score, 0, 100, 90, 0);
    gaugeServo.write(targetAngle);

    // Hold reading posture with tier LED feedback for 5 seconds (5000 ms)
    unsigned long startTime = millis();
    while (millis() - startTime < 5000) {
      if (score < 45) {
        // Tier 1 (<45): Solid ON
        digitalWrite(LED_PIN, HIGH);
        delay(100);
      } else if (score < 75) {
        // Tier 2 (45-74): Warning blinks (250ms ON / 250ms OFF)
        digitalWrite(LED_PIN, HIGH);
        delay(250);
        digitalWrite(LED_PIN, LOW);
        delay(250);
      } else {
        // Tier 3 (>=75): Rapid alert strobe (100ms ON / 100ms OFF)
        digitalWrite(LED_PIN, HIGH);
        delay(100);
        digitalWrite(LED_PIN, LOW);
        delay(100);
      }
    }

    // After 5 seconds, return servo smoothly to rest position (90°) and turn off LED
    gaugeServo.write(90);
    digitalWrite(LED_PIN, LOW);

    // Flush remaining serial input
    while (Serial.available() > 0) {
      Serial.read();
    }
  }
}

