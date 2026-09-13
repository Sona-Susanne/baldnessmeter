<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />

# Baldness-o-Meter 🎯

## Basic Details

### Team Name: Askaban Asteroid

### Team Members
- Team Lead: Sona Susan Jacob - Saintgits College of Engineering

### Project Description
An AI-powered diagnostic and physical hardware gauge that quantifies cranial follicular density in real-time. By combining MediaPipe 3D face mesh tracking, dynamic visual intensity gradient edge detection, and OpenCV image processing, it calculates forehead surface ratios and transmits real-time hairline reality checks over PySerial (COM6) directly to a physical servo dial and diagnostic LED array.

### The Problem (that doesn't exist)
In a world overflowing with optical illusions and deceptive camera angles, unsuspecting individuals live under the catastrophic delusion that their forehead is merely "broad" rather than an international football ground. Humanity has long suffered from the lack of an unscientific, overly sensitive, Malayalam-calibrated physical meter to call out receding hairlines before gentle breezes cause irreversible aerodynamic drag.

### The Solution (that nobody asked for)
The Baldness-o-Meter pairs a webcam with MediaPipe 3D face mesh tracking and a Gaussian 1D intensity gradient edge finder to calculate forehead geometry with a humorously boosted sensitivity curve. The calculated hazard score is displayed across a cyberpunk HUD in native Malayalam/Manglish commentary and dispatched via USB Serial (COM6) to an Arduino Uno, driving a servo needle across a calibrated physical paper dial ranging from "SAFE ZONE" to "NE SOOKSHIKANAM", "ORU FOOTBALL KALIKALLO IVIDE", and "NE TEERNU • YOU ARE DONE".

## Technical Details
### Technologies/Components Used
For Software:
- Languages: Python 3.10+, C++ (Arduino Wiring)
- Frameworks: OpenCV (`cv2`)
- Libraries: MediaPipe (FaceMesh / 3D Facial Geometry), PySerial, NumPy
- Tools: VS Code, Arduino IDE, Git & GitHub

For Hardware:
- Main Components:
  - Arduino Uno Rev3 / Nano (COM6 @ 9600 Baud)
  - TowerPro SG90 9g Micro Servo Motor
  - 5mm Red Diagnostic Indicator LED
  - 220-ohm Resistor
  - Breadboard & Jumper Wires
  - Custom Calibrated Paper Gauge Meter Dial
- Specifications:
  - Baud Rate: 9600 bps over Serial (COM6)
  - Needle Sweep: Inverted 0°–180° mapping (180° = Safe to 0° = Done)
  - Operating Voltage: 5V DC via USB
- Tools Required: USB Cable, Marker pen, Card stock

### How the Computer Vision Works (The Facial Ratio & Edge Finder Algorithm)
The system uses MediaPipe Face Mesh with OpenCV to track 468 landmark coordinates across the user's face in real-time. Rather than measuring raw pixels (which change when leaning closer or further from the camera), it calculates an invariant geometric vertical ratio:

1. **Dynamic Hairline Edge Finder**:
   - Extracts a vertical slice of grayscale forehead pixels between the eyebrow center (midpoint of landmarks 107 & 336 / landmark 9) and the cranial apex (landmark 10).
   - Applies a 1D Gaussian blur filter to smooth lighting shifts.
   - Finds the maximum intensity gradient transition edge where dark hair drops off into bright forehead skin (`y_hairline`).

2. **Distance & Ratio Calculations**:
   - Forehead Height: Vertical distance between eyebrow center and `y_hairline`.
   - Facial Height: Vertical distance between eyebrow center and chin baseline (landmark 152).
   - Anatomical Ratio = Forehead Height / max(0.001, Facial Height).

3. **Temporal Median Filtering & Sensitivity Scaling**:
   - Accumulates ratio samples during the 2.0-second scan window and calculates `np.median(ratios)` to reject frame noise and micro-movements.
   - Applies a humorous sensitivity curve boost:
     `calculated_score = (median_ratio - 0.08) * 210.0 + 10.0`
     `final_score = int(np.clip((calculated_score * 1.4) + 15, 0, 100))`

### Implementation
For Software:
# Installation
```bash
git clone https://github.com/Sona-Susanne/baldnessmeter.git
cd baldnessmeter
pip install opencv-python mediapipe numpy pyserial
```

# Run
1. Connect Arduino to computer via USB (Port: COM6).
2. Upload `arduino_gauge.ino` using Arduino IDE and close the IDE serial monitor.
3. Run the Python application:
```bash
python baldness_o_meter.py
```
4. Look into the webcam and press `[SPACEBAR]` to trigger a 2-second scan. Press `q` or `[ESC]` to exit.

### Project Documentation
For Software:

# Screenshots
<img width="1920" height="1080" alt="Screenshot (2)" src="https://github.com/user-attachments/assets/e03e9521-39a5-47ea-a83d-e684fb6342b0" />
*Progressive scan phase diagnostics HUD with bottom animated progress bar.*

<img width="1920" height="1080" alt="Screenshot (3)" src="https://github.com/user-attachments/assets/00f48cc2-e4fe-4e22-8319-61217d4220d7" />
*Results lock screen displaying Malayalam verdict badge and aerodynamic metrics card.*

<img width="1920" height="1080" alt="Screenshot (4)" src="https://github.com/user-attachments/assets/54e892fa-46d5-4b02-8ed8-42f2ed6e8f6b" />
*High baldness index result screen.*

For Hardware:

# Schematic & Circuit
<img width="3060" height="4080" alt="1000210574" src="https://github.com/user-attachments/assets/37598021-4453-42c5-ad68-e1d276ef31ce" />

# Build Photos
<img width="4080" height="3060" alt="1000210575" src="https://github.com/user-attachments/assets/ec3b444f-b875-4824-9746-24ba0b6b6d6a" />
*Hardware setup and physical gauge assembly.*

### Project Demo
# Video
https://drive.google.com/file/d/1ASnoFL76eG3gU7j8GqUSllofjtB_xwYb/view?usp=drivesdk

## Team Contributions
- Sona Susan Jacob: End-to-end concept design, MediaPipe facial mesh tracking implementation, PySerial hardware communication protocol, Arduino firmware programming, physical paper gauge calibration, and testing.

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)
