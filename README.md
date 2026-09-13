<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />

# Baldness-o-Meter 

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

---

## Technical Details
### Technologies/Components Used
For Software:
- Languages: Python 3.10+, C++ (Arduino Wiring)
- Frameworks: OpenCV (`cv2`)
- Libraries: MediaPipe (FaceMesh / 3D Facial Geometry), PySerial, NumPy
- Tools: VS Code, Arduino IDE, Git & GitHub

For Hardware:
- Main Components:
  - Arduino Uno Rev3
  - TowerPro SG90 9g Micro Servo Motor
  - 5mm Red Diagnostic Indicator LED
  - 220Ω Resistor
  - Breadboard & Jumper Wires
  - Custom Calibrated 3-Sector Paper Gauge (Top-to-Right sweep)
- Specifications:
  - Baud Rate: 9600 bps over Serial (COM6)
  - Needle Sweep: Vertical/Top (25-45% BALD) to Horizontal/Right (75-100% BALD DANGER ZONE)
  - Operating Voltage: 5V DC via USB
- Tools Required: USB Type-A to Type-B cable, Marker pen, Paper card stock

---

### How the Computer Vision Works (The Facial Ratio Algorithm)

The system uses **MediaPipe Face Mesh** with OpenCV to track 468 landmark coordinates across the user's face in real-time. Rather than measuring raw pixels (which change when leaning closer or further from the camera), it calculates an invariant **geometric vertical ratio**:

1. **Landmark Extraction:**
   - **Mid-Eyebrow Center:** Landmark 9 (glabella / brow line)
   - **Trichion / Upper Forehead Boundary:** Landmark 10 (top-most scalp tracker)
   - **Chin Base (Menton):** Landmark 152 (bottom tip of the jaw)

2. **Distance Calculations:**
   - **Forehead Height ($H_{\text{forehead}}$):** Euclidean vertical distance between the eyebrow line (Landmark 9) and the upper forehead boundary (Landmark 10).
   - **Total Facial Height ($H_{\text{face}}$):** Euclidean vertical distance between the chin base (Landmark 152) and the upper forehead boundary (Landmark 10).

3. **Ratio Metric & Sensitivity Scaling:**
   $$\text{Forehead Ratio} = \frac{H_{\text{forehead}}}{H_{\text{face}}}$$
   - In classical facial aesthetics (the Rule of Thirds), the forehead should occupy approximately **33%** ($\sim 0.33$) of total vertical face height.
   - The algorithm normalizes any ratio above the aesthetic baseline and applies a non-linear sensitivity scaling multiplier:
   $$\text{Raw Score} = \left(\frac{\text{Forehead Ratio} - 0.22}{0.18}\right) \times 100$$
   $$\text{Final Exaggerated Score} = \text{clamp}((\text{Raw Score} \times 1.4) + 20,\ 0,\ 100)$$
   This ensures minor natural hairline variations immediately boost the output into the humorous **"50-70% BALD"** or **"75-100% BALD (DANGER ZONE)"** thresholds.

---

### Implementation
For Software:

# Installation
```bash
# Clone the repository
git clone <your-repository-url>
cd baldness_o_meter

# Install dependencies
pip install opencv-python mediapipe pyserial numpy

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)



