<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />

# Baldness-o-Meter 🎯


## Basic Details

### Team Name: Askaban Asteroid


### Team Members
- Team Lead: Sona Susan Jacob - Saintgits College of Engineering

### Project Description
An AI-powered diagnostic and physical hardware gauge that quantifies cranial follicular density in real-time. By leveraging computer vision and aerodynamic facial geometry estimation, it transmits severe scalp reality checks directly to a physical servo dial and diagnostic LED array.

### The Problem (that doesn't exist)
In a world overflowing with optical illusions and deceptive camera angles, unsuspecting individuals live under the catastrophic delusion that their forehead is merely "broad" rather than an international football ground. Humanity has long suffered from the lack of an unscientific, overly sensitive, Malayalam-calibrated physical meter to call out receding hairlines before gentle breezes cause irreversible aerodynamic drag.

### The Solution (that nobody asked for)
The Baldness-o-Meter pairs a webcam with MediaPipe 3D face mesh tracking to calculate forehead surface area with an exaggerated sensitivity curve. The calculated hazard score is displayed across a cyberpunk HUD in native Manglish commentary and dispatched via USB Serial (COM6) to an Arduino Uno, driving a servo needle across a 3-tier calibrated paper dial ranging from "25-45% BALD" to "50-70% BALD" and finally "75-100% BALD (DANGER ZONE)".

## Technical Details
### Technologies/Components Used
For Software:
- Languages: Python 3.10+, C++ (Arduino Wiring)
- Frameworks: OpenCV (cv2)
- Libraries: MediaPipe (FaceMesh / 3D Facial Geometry), PySerial, NumPy
- Tools: VS Code, Arduino IDE, Git & GitHub

For Hardware:
- Main Components:
  - Arduino Uno Rev3
  - TowerPro SG90 9g Micro Servo Motor
  - 5mm Red Diagnostic Indicator LED
  - 220-ohm Resistor
  - Breadboard & Jumper Wires
  - Custom Calibrated 3-Sector Paper Gauge (Top-to-Right sweep)
- Specifications:
  - Baud Rate: 9600 bps over Serial (COM6)
  - Needle Sweep: Vertical/Top (25-45% BALD) to Horizontal/Right (75-100% BALD DANGER ZONE)
  - Operating Voltage: 5V DC via USB
- Tools Required: USB Type-A to Type-B cable, Marker pen, Paper card stock

### How the Computer Vision Works (The Facial Ratio Algorithm)
The system uses MediaPipe Face Mesh with OpenCV to track 468 landmark coordinates across the user's face in real-time. Rather than measuring raw pixels (which change when leaning closer or further from the camera), it calculates an invariant geometric vertical ratio:

1. Landmark Extraction:
   - Mid-Eyebrow Center: Landmark 9 (glabella / brow line)
   - Trichion / Upper Forehead Boundary: Landmark 10 (top-most scalp tracker)
   - Chin Base (Menton): Landmark 152 (bottom tip of the jaw)

2. Distance Calculations:
   - Forehead Height: Vertical distance between Landmark 9 (eyebrows) and Landmark 10 (upper forehead boundary).
   - Total Facial Height: Vertical distance between Landmark 152 (chin) and Landmark 10 (upper forehead boundary).

3. Ratio Metric & Sensitivity Scaling:
   - Ratio = Forehead Height / Total Facial Height
   - Under standard aesthetic facial proportions (the Rule of Thirds), the forehead typically occupies roughly 33% (0.33) of the vertical face height.
   - The algorithm normalizes any ratio against a baseline floor of 0.22, normalizes it over an 0.18 band, and applies a non-linear sensitivity scaling boost:
     Final Score = clamp(((Raw Ratio - 0.22) / 0.18 * 100) * 1.4 + 20, 0, 100)
   - This ensures even minor natural hairline variations push the reading into the humorous "50-70% BALD" or "75-100% BALD (DANGER ZONE)" sectors.

### Implementation
For Software:
# Installation
git clone <your-repository-url>
cd baldness_o_meter
pip install opencv-python mediapipe pyserial numpy

# Run
1. Connect Arduino Uno to the computer via USB (Port: COM6).
2. Upload arduino_gauge.ino using Arduino IDE and make sure the IDE is closed.
3. Execute the Python application:
python baldness_o_meter.py
4. Look into the webcam and press [SPACE] to trigger a scan cycle. Press q or [ESC] to exit.

### Project Documentation
For Software:

# Screenshots (Add at least 3)
![Screenshot1](screenshots/scan_phase.png)
<img width="1920" height="1080" alt="Screenshot (2)" src="https://github.com/user-attachments/assets/e03e9521-39a5-47ea-a83d-e684fb6342b0" />

![Screenshot2](screenshots/result_mid.png)
<img width="1920" height="1080" alt="Screenshot (3)" src="https://github.com/user-attachments/assets/00f48cc2-e4fe-4e22-8319-61217d4220d7" />

![Screenshot3](screenshots/result_danger.png)
<img width="1920" height="1080" alt="Screenshot (4)" src="https://github.com/user-attachments/assets/54e892fa-46d5-4b02-8ed8-42f2ed6e8f6b" />


For Hardware:

# Schematic & Circuit
<img width="3060" height="4080" alt="1000210574" src="https://github.com/user-attachments/assets/37598021-4453-42c5-ad68-e1d276ef31ce" />



# Build Photos
<img width="4080" height="3060" alt="1000210575" src="https://github.com/user-attachments/assets/ec3b444f-b875-4824-9746-24ba0b6b6d6a" />

![Build](hardware/build_process.jpg)
*Calibrating servo horn zero-position and mapping vertical top (25-45%) to horizontal right (75-100%).*

![Final](hardware/final_build.jpg)
*Completed physical paper gauge mounted with active SG90 indicator arm pointing at the 3 sectors.*

### Project Demo
# Video

https://drive.google.com/file/d/1ASnoFL76eG3gU7j8GqUSllofjtB_xwYb/view?usp=drivesdk

# Additional Demos
- Dynamic reaction images corresponding to the 3 dial sectors.
- Inverted servo sweep benchmark from top vertical position down to right horizontal angle.

## Team Contributions
- Sona Susan Jacob: End-to-end concept design, MediaPipe facial mesh tracking implementation, PySerial hardware communication protocol, Arduino firmware programming, physical paper gauge calibration, and testing.

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)
---


