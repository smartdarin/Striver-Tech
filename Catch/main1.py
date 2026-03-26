import cv2
import numpy as np
import time
from sklearn.linear_model import LinearRegression
import pandas as pd

# ----------------------------
# 🔹 Video Input
# ----------------------------
cap = cv2.VideoCapture("video1.mp4")

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# ----------------------------
# 🔹 Data Storage
# ----------------------------
counts = []
times = []
start_time = time.time()

# ----------------------------
# 🔹 Prediction Function
# ----------------------------
def predict_future(counts):
    if len(counts) < 5:
        return None

    X = np.array(range(len(counts))).reshape(-1, 1)
    y = np.array(counts)

    model = LinearRegression()
    model.fit(X, y)

    return int(model.predict([[len(counts) + 5]])[0])

# ----------------------------
# 🔹 SMART ZONE DENSITY (FIXED)
# ----------------------------
def zone_density(zone):
    gray = cv2.cvtColor(zone, cv2.COLOR_BGR2GRAY)

    # Edge detection (captures human boundaries)
    edges = cv2.Canny(gray, 50, 150)

    # Texture detection (crowd = high variation)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    texture = np.mean(np.abs(laplacian))

    edge_density = np.sum(edges > 0) / (zone.shape[0] * zone.shape[1])

    # Combine signals
    density = (edge_density * 0.7) + ((texture / 255) * 0.3)

    return density

# ----------------------------
# 🔹 MAIN LOOP
# ----------------------------
while True:
    ret, frame = cap.read()

    # Loop video
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    frame = cv2.resize(frame, (800, 600))
    display = frame.copy()

    h, w, _ = frame.shape

    # ----------------------------
    # 🔥 HEATMAP
    # ----------------------------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (15, 15), 0)
    heatmap = cv2.applyColorMap(blur, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(display, 0.6, heatmap, 0.4, 0)

    # ----------------------------
    # 🔹 ZONE SPLIT
    # ----------------------------
    left = frame[:, :w//3]
    mid = frame[:, w//3:2*w//3]
    right = frame[:, 2*w//3:]

    ld = zone_density(left)
    md = zone_density(mid)
    rd = zone_density(right)

    # ----------------------------
    # 🔥 USE MAX (CRITICAL FIX)
    # ----------------------------
    raw_density = max(ld, md, rd)

# Normalize (IMPORTANT)
    occupancy = min(raw_density * 2.5, 1.0)

    # Identify hotspot zone
    zone_vals = {"LEFT": ld, "MID": md, "RIGHT": rd}
    hotspot = max(zone_vals, key=zone_vals.get)

    # ----------------------------
    # 🔹 PEOPLE ESTIMATION (UPDATED)
    # ----------------------------
    people = int(occupancy * 400)

    # ----------------------------
    # 🔥 DYNAMIC CAPACITY
    # ----------------------------
    free_space = 1 - occupancy
    capacity = int((free_space + 0.2) * 300)

    # ----------------------------
    # 🔹 STORE DATA
    # ----------------------------
    t = time.time() - start_time
    counts.append(people)
    times.append(t)

    if len(counts) > 100:
        counts.pop(0)
        times.pop(0)

    pred = predict_future(counts)

    # ----------------------------
    # 🔥 INTELLIGENT DECISION SYSTEM
    # ----------------------------
    if occupancy > 0.65:
        status = "CRITICAL"
        color = (0, 0, 255)

    elif occupancy > 0.5:
        status = "HIGH"
        color = (0, 165, 255)

    elif occupancy > 0.35:
        status = "MODERATE"
        color = (0, 255, 255)

    else:
        status = "SAFE"
        color = (0, 255, 0)

    # ----------------------------
    # 🔹 DISPLAY
    # ----------------------------
    cv2.putText(overlay, f"People: {people}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.putText(overlay, f"Capacity: {capacity}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

    cv2.putText(overlay, f"Occupancy: {occupancy:.2f}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (200,255,200), 2)

    cv2.putText(overlay, f"Zone: {hotspot}", (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.putText(overlay, status, (20, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    if pred:
        cv2.putText(overlay, f"Predicted: {pred}", (20, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)

        if pred > capacity:
            cv2.putText(overlay, "FUTURE RISK!", (20, 280),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

    # Zone lines
    cv2.line(overlay, (w//3, 0), (w//3, h), (255,255,255), 2)
    cv2.line(overlay, (2*w//3, 0), (2*w//3, h), (255,255,255), 2)

    # ----------------------------
    # 🔹 SHOW OUTPUT
    # ----------------------------
    cv2.imshow("AI Crowd Intelligence", overlay)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# ----------------------------
# 🔹 SAVE DATA FOR DASHBOARD
# ----------------------------
df = pd.DataFrame({"time": times, "count": counts})
df.to_csv("crowd_data.csv", index=False)

cap.release()
cv2.destroyAllWindows()