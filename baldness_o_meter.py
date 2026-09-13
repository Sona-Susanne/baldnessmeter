"""
Baldness-O-Meter 3000
=====================
High-precision 3D MediaPipe Face Mesh follicle tracker with progressive "scientific"
diagnostics, clean multi-card HUD results, Spacebar trigger workflow, and PySerial COM6 Arduino control.
"""

import cv2
import numpy as np
import mediapipe.python.solutions.face_mesh as mp_face_mesh
import mediapipe.python.solutions.drawing_utils as mp_drawing
import serial
import time
import math
import sys


def draw_hud_card(img, x, y, w, h, bg_color=(15, 15, 25), border_color=(0, 255, 255), alpha=0.85):
    """Draws a sleek translucent HUD card with a subtle border for text background readability."""
    h_img, w_img = img.shape[:2]
    x1 = max(0, min(x, w_img - 1))
    y1 = max(0, min(y, h_img - 1))
    x2 = max(x1 + 1, min(x + w, w_img))
    y2 = max(y1 + 1, min(y + h, h_img))

    sub_img = img[y1:y2, x1:x2]
    card_rect = np.full(sub_img.shape, bg_color, dtype=np.uint8)
    res = cv2.addWeighted(sub_img, 1.0 - alpha, card_rect, alpha, 0)
    img[y1:y2, x1:x2] = res
    cv2.rectangle(img, (x1, y1), (x2 - 1, y2 - 1), border_color, 1)


def get_ridiculous_classification(score):
    """Returns classification title based on score tier."""
    if score <= 25:
        return "SAFE ZONE"
    elif score <= 50:
        return "NE SOOKSHIKANAM"
    elif score <= 75:
        return "ORU FOOTBALL KALIKALLO IVIDE"
    else:
        return "NE TEERNU - YOU ARE DONE"


def get_hair_status_label(score):
    """Returns status text based on score."""
    if score <= 25:
        return "HAIR STATUS: APPROVED"
    elif score <= 55:
        return "HAIR STATUS: WE HAVE CONCERNS"
    else:
        return "EMERGENCY: HAIR HAS LEFT THE CHAT"


def get_scan_diagnostic_text(elapsed):
    """Returns progressive scientific diagnostic text synchronized across 2-second scan."""
    if elapsed < 0.4:
        return "NETTIYUDE VISTHEERTHAM ALAKKUNNU..."
    elif elapsed < 0.8:
        return "THALA MUDI THAPPUNNU (SCANNING)..."
    elif elapsed < 1.2:
        return "KATTINTE RESISTANCE CALCULATE CHEYYUNNU..."
    elif elapsed < 1.6:
        return "CONSULTING GLOBAL HAIR DATABASE..."
    else:
        return "ERROR: DATABASE HAS NO OPINION."


def main():
    print("=== Baldness-O-Meter 3000 (MediaPipe 3D Mesh) Starting ===")

    # Initialize MediaPipe Face Mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    # Initialize CLAHE contrast equalizer
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    # Initialize PySerial Connection directly on COM6
    arduino = None
    try:
        arduino = serial.Serial('COM6', 9600, timeout=1)
        time.sleep(2.0)  # Mandatory: wait for Arduino reboot cycle
        print("[HARDWARE] Successfully connected to Arduino on COM6!")
    except Exception as e:
        print(f"[HARDWARE ERROR] Could not connect to COM6: {e}")

    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[Error] Could not open webcam (index 0). Please check your camera connection.")
        sys.exit(1)

    print("Webcam started. Press [SPACE] to trigger scan. Press 'q' to quit.")

    # State Machine Variables
    # States: "STANDBY", "SCANNING", "RESULT"
    state = "STANDBY"
    scan_start_time = 0
    SCAN_DURATION = 2.0  # seconds

    sampled_ratios = []
    final_score = 0
    classification = ""
    status_label = ""
    last_forehead_edges_preview = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[Warning] Failed to grab frame from webcam.")
            break

        # Flip horizontally for intuitive mirror display
        frame = cv2.flip(frame, 1)
        h_frame, w_frame = frame.shape[:2]

        # Convert to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_clahe = clahe.apply(gray)

        detected_face = False
        current_ratio = 0.0

        if results.multi_face_landmarks and len(results.multi_face_landmarks) > 0:
            detected_face = True
            landmarks = results.multi_face_landmarks[0].landmark

            # Helper to convert normalized landmark to pixel tuple
            def get_pt(idx):
                lm = landmarks[idx]
                return (int(lm.x * w_frame), int(lm.y * h_frame))

            # Key 3D Anatomical Landmarks:
            # 1. Hairline apex / Forehead peak (landmark 10)
            p10 = get_pt(10)
            # 2. Chin baseline (landmark 152)
            p152 = get_pt(152)
            # 3. Eyebrow midpoint (average of 107 and 336)
            p107 = get_pt(107)
            p336 = get_pt(336)
            eyebrow_midpoint = ((p107[0] + p336[0]) // 2, (p107[1] + p336[1]) // 2)
            # 4. Temple markers (234 and 454)
            p234 = get_pt(234)
            p454 = get_pt(454)

            # Additional forehead contour points for smooth polygon definition
            p67 = get_pt(67)
            p109 = get_pt(109)
            p338 = get_pt(338)
            p297 = get_pt(297)

            # 1. Dynamic Hairline Edge Finder along Forehead Midline:
            x_mid = eyebrow_midpoint[0]
            y_top = min(p10[1], eyebrow_midpoint[1])
            y_brow = max(p10[1], eyebrow_midpoint[1])

            y_hairline = y_top  # Default fallback if no gradient edge found

            if (y_brow - y_top) > 10:
                x1 = max(0, x_mid - 4)
                x2 = min(w_frame, x_mid + 5)
                slice_2d = gray_clahe[y_top:y_brow, x1:x2]

                if slice_2d.size > 0:
                    profile_1d = np.mean(slice_2d, axis=1)
                    profile_smoothed = cv2.GaussianBlur(profile_1d.reshape(-1, 1), (1, 5), 0).flatten()
                    gradient = np.gradient(profile_smoothed)

                    # Find transition edge (maximum positive gradient: dark hair -> bright forehead skin)
                    max_grad_idx = int(np.argmax(gradient))
                    y_hairline = y_top + max_grad_idx

            # 2. Recalculate Forehead Proportion based on true visual hairline position:
            forehead_h = abs(eyebrow_midpoint[1] - y_hairline)
            face_h = math.hypot(eyebrow_midpoint[0] - p152[0], eyebrow_midpoint[1] - p152[1])
            current_ratio = forehead_h / max(0.001, face_h)

            # 3. Precise Forehead Polygon Crop & Canny Edge Texture
            poly_pts = np.array([p107, p67, p109, p10, p338, p297, p336], dtype=np.int32)

            mask = np.zeros((h_frame, w_frame), dtype=np.uint8)
            cv2.fillPoly(mask, [poly_pts], 255)

            edges = cv2.Canny(gray_clahe, 50, 150)
            forehead_edges = cv2.bitwise_and(edges, edges, mask=mask)
            last_forehead_edges_preview = forehead_edges

            # Draw 3D Mesh / Landmarks Visual Overlay
            mesh_color = (0, 255, 0) if state == "RESULT" else ((0, 255, 255) if state == "SCANNING" else (0, 200, 255))

            # Forehead polygon outline
            cv2.polylines(frame, [poly_pts], True, mesh_color, 2)

            # Anatomical midline & temple alignment lines
            cv2.line(frame, eyebrow_midpoint, (x_mid, y_hairline), (255, 255, 0), 1)
            cv2.line(frame, eyebrow_midpoint, p152, (255, 255, 0), 1)
            cv2.line(frame, p234, p454, (255, 0, 255), 1)

            # 4. Visual Verification Marker: Draw horizontal cyan line across true visual y_hairline
            marker_w = 40
            cv2.line(frame, (x_mid - marker_w // 2, y_hairline), (x_mid + marker_w // 2, y_hairline), (255, 255, 0), 2)
            cv2.putText(frame, "TRUE HAIRLINE", (x_mid + marker_w // 2 + 5, y_hairline + 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 0), 1)

            # Key landmark dots
            for pt in [p10, p152, eyebrow_midpoint, p234, p454, p107, p336]:
                cv2.circle(frame, pt, 4, (0, 255, 255), -1)

        # --- State Machine Update ---
        now = time.time()

        if state == "SCANNING":
            if detected_face and current_ratio > 0:
                sampled_ratios.append(current_ratio)

            elapsed_scan = now - scan_start_time
            if elapsed_scan >= SCAN_DURATION:
                state = "RESULT"

                if len(sampled_ratios) > 0:
                    # Temporal Median Filtering (Zero Drift) across 2-second scan
                    median_ratio = float(np.median(sampled_ratios))
                else:
                    median_ratio = 0.12

                # Dynamic Visual Hairline Proportion Score Mapping (humorous threshold boost)
                calculated_score = (median_ratio - 0.08) * 210.0 + 10.0
                boosted_score = (calculated_score * 1.4) + 15.0
                final_score = int(round(np.clip(boosted_score, 0.0, 100.0)))
                classification = get_ridiculous_classification(final_score)
                status_label = get_hair_status_label(final_score)

                # Send score directly to COM6 Arduino ONCE upon locking result
                if arduino and arduino.is_open:
                    try:
                        payload = f"{int(final_score)}\n".encode('utf-8')
                        arduino.write(payload)
                        arduino.flush()
                        print(f"[HARDWARE] Sent score {int(final_score)} to COM6")
                    except Exception as e:
                        print(f"[HARDWARE ERROR] Failed to send data to COM6: {e}")

        # --- Keyboard Inputs ---
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # 'q' or ESC
            break
        elif key == 32:  # SPACEBAR trigger
            if state == "STANDBY" and detected_face:
                state = "SCANNING"
                scan_start_time = time.time()
                sampled_ratios = []
            elif state == "RESULT":
                state = "STANDBY"
                sampled_ratios = []

        # --- Draw Non-Overlapping HUD UI ---

        # 1. Top Header Card (Title & Branding)
        draw_hud_card(frame, 20, 15, 330, 48, bg_color=(15, 15, 25), border_color=(0, 255, 255), alpha=0.85)
        cv2.putText(frame, "BALDNESS-O-METER 3000", (32, 36),
                    cv2.FONT_HERSHEY_DUPLEX, 0.65, (0, 255, 255), 2)
        cv2.putText(frame, "3D MESH FOLLICLE TRACKER", (32, 54),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, (180, 180, 180), 1)

        # 2. Top Right Inset (Canny Edges Preview)
        if last_forehead_edges_preview is not None:
            inset_w, inset_h = 120, 85
            inset_x, inset_y = w_frame - inset_w - 20, 15
            draw_hud_card(frame, inset_x - 5, inset_y - 5, inset_w + 10, inset_h + 22,
                          bg_color=(10, 10, 15), border_color=(0, 255, 0), alpha=0.85)

            canny_bgr = cv2.cvtColor(last_forehead_edges_preview, cv2.COLOR_GRAY2BGR)
            canny_resized = cv2.resize(canny_bgr, (inset_w, inset_h))
            frame[inset_y:inset_y + inset_h, inset_x:inset_x + inset_w] = canny_resized

            cv2.putText(frame, "3D FOREHEAD CANNY", (inset_x - 2, inset_y + inset_h + 14),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.36, (0, 255, 0), 1)

        # 3. Serial Status Badge (Bottom-Right)
        com_connected = (arduino is not None and arduino.is_open)
        com_str = f"COM6: {'CONNECTED' if com_connected else 'DISCONNECTED'}"
        com_color = (0, 255, 0) if com_connected else (0, 0, 255)
        draw_hud_card(frame, w_frame - 200, h_frame - 35, 180, 25, bg_color=(10, 10, 15), border_color=com_color, alpha=0.85)
        cv2.putText(frame, com_str, (w_frame - 192, h_frame - 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, com_color, 1)

        # 4. Contextual State-Driven HUD Layouts

        if not detected_face:
            # NO FACE State: Clean centered banner
            card_w, card_h = 440, 55
            card_x = (w_frame - card_w) // 2
            card_y = h_frame - 90
            draw_hud_card(frame, card_x, card_y, card_w, card_h, bg_color=(25, 15, 15), border_color=(0, 165, 255), alpha=0.85)
            cv2.putText(frame, "POSITION SUBJECT IN FRAME TO BEGIN", (card_x + 22, card_y + 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 215, 255), 2)

        elif state == "STANDBY":
            # STANDBY State: Bottom HUD prompt waiting for SPACEBAR
            card_w, card_h = w_frame - 240, 55
            card_x = 40
            card_y = h_frame - 90
            draw_hud_card(frame, card_x, card_y, card_w, card_h, bg_color=(15, 25, 20), border_color=(0, 255, 255), alpha=0.85)
            cv2.putText(frame, "SUBJECT LOCKED • PRESS [SPACE] TO SCAN", (card_x + 20, card_y + 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.58, (0, 255, 255), 2)

        elif state == "SCANNING":
            # SCANNING State: Progressive Scientific Diagnostic Lines & Progress Bar
            elapsed_scan = now - scan_start_time
            progress_pct = min(100.0, (elapsed_scan / SCAN_DURATION) * 100.0)
            diagnostic_text = get_scan_diagnostic_text(elapsed_scan)

            card_w, card_h = w_frame - 240, 75
            card_x = 40
            card_y = h_frame - 110
            draw_hud_card(frame, card_x, card_y, card_w, card_h, bg_color=(20, 20, 30), border_color=(0, 255, 255), alpha=0.9)

            # Progressive Scientific Diagnostic Line
            cv2.putText(frame, diagnostic_text, (card_x + 15, card_y + 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 255, 255), 2)

            # Animated Progress Bar
            pbar_x = card_x + 15
            pbar_y = card_y + 38
            pbar_w = card_w - 30
            pbar_h = 22
            fill_w = int((progress_pct / 100.0) * pbar_w)

            cv2.rectangle(frame, (pbar_x, pbar_y), (pbar_x + pbar_w, pbar_y + pbar_h), (40, 40, 50), -1)
            cv2.rectangle(frame, (pbar_x, pbar_y), (pbar_x + fill_w, pbar_y + pbar_h), (0, 255, 255), -1)
            cv2.rectangle(frame, (pbar_x, pbar_y), (pbar_x + pbar_w, pbar_y + pbar_h), (255, 255, 255), 1)

            prog_text = f"{int(progress_pct)}% COMPLETE"
            cv2.putText(frame, prog_text, (pbar_x + 15, pbar_y + 16),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)

        elif state == "RESULT":
            # RESULT State: Comprehensive Clean Multi-Card HUD Layout

            # Card A: Primary Verdict & Title Badge (Upper Left / Center)
            cardA_w, cardA_h = 370, 92
            cardA_x = 20
            cardA_y = 70
            score_color = (0, 255, 0) if final_score < 40 else ((0, 165, 255) if final_score < 75 else (0, 0, 255))
            draw_hud_card(frame, cardA_x, cardA_y, cardA_w, cardA_h, bg_color=(15, 25, 20), border_color=score_color, alpha=0.9)

            cv2.putText(frame, f"BALDNESS INDEX: {final_score}%", (cardA_x + 15, cardA_y + 28),
                        cv2.FONT_HERSHEY_DUPLEX, 0.65, score_color, 2)
            cv2.putText(frame, f"CLASSIFICATION: {classification}", (cardA_x + 15, cardA_y + 54),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.46, (0, 255, 255), 2)
            cv2.putText(frame, f"{status_label}", (cardA_x + 15, cardA_y + 78),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)

            # Card B: Useless Statistics Card (Side / Lower Left)
            cardB_w, cardB_h = 370, 105
            cardB_x = 20
            cardB_y = 172
            draw_hud_card(frame, cardB_x, cardB_y, cardB_w, cardB_h, bg_color=(12, 16, 24), border_color=(0, 255, 180), alpha=0.88)

            stat_line1 = f"HAIR NEEDED: {final_score * 68} UNITS"
            stat_line2 = "ESTIMATED REGROWTH: ADUTHA JANMAM"
            stat_line3 = "WIND RESISTANCE: OPTIMAL FOR FLIGHT"
            stat_line4 = "AI CONFIDENCE: 11% | REASON: ARIYILLA"

            for i, line_str in enumerate([stat_line1, stat_line2, stat_line3, stat_line4]):
                cv2.putText(frame, line_str, (cardB_x + 15, cardB_y + 24 + (i * 22)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.38, (200, 230, 255), 1)

            # Card C: Disclaimer Footer (Bottom of Screen)
            cardC_w, cardC_h = w_frame - 40, 46
            cardC_x = 20
            cardC_y = h_frame - 60
            draw_hud_card(frame, cardC_x, cardC_y, cardC_w, cardC_h, bg_color=(15, 15, 20), border_color=(0, 255, 255), alpha=0.9)

            disclaimer_str = "DISCLAIMER: Absolutely no medical validity. Trust at your own risk."
            cv2.putText(frame, disclaimer_str, (cardC_x + 15, cardC_y + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.38, (200, 200, 200), 1)
            cv2.putText(frame, "PRESS [SPACE] FOR NEXT SUBJECT", (cardC_x + 15, cardC_y + 38),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 255, 255), 2)

        cv2.imshow("Baldness-O-Meter 3000 (3D Mesh)", frame)

    cap.release()
    cv2.destroyAllWindows()
    face_mesh.close()
    if arduino and arduino.is_open:
        arduino.close()
        print("[HARDWARE] Serial connection on COM6 closed cleanly.")
    print("=== Baldness-O-Meter Terminated Gracefully ===")


if __name__ == "__main__":
    main()
