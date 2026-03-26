import cv2
import numpy as np
import pandas as pd
import time
from ultralytics import YOLO
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# ----------------------------
# 🔹 Load YOLO Model
# ----------------------------
model = YOLO("yolov8l.pt")

# ----------------------------
# 🔹 Video Input (use webcam or video file)
# ----------------------------
cap = cv2.VideoCapture(0)  # 0 for webcam, or "video.mp4"

# ----------------------------
# 🔹 Data Storage
# ----------------------------
timestamps = []
counts = []

start_time = time.time()

# ----------------------------
# 🔹 Prediction Function
# ----------------------------
def predict_future(counts):
    if len(counts) < 5:
        return None

    X = np.array(range(len(counts))).reshape(-1, 1)
    y = np.array(counts)

    model_lr = LinearRegression()
    model_lr.fit(X, y)

    future_index = np.array([[len(counts) + 5]])
    prediction = model_lr.predict(future_index)

    return int(prediction[0])

# ----------------------------
# 🔹 Main Loop
# ----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    people_count = 0

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])

            # Class 0 = person in COCO dataset
            if cls == 0:
                people_count += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

    # ----------------------------
    # Store Data
    # ----------------------------
    current_time = time.time() - start_time
    timestamps.append(current_time)
    counts.append(people_count)

    # ----------------------------
    # Predict Future
    # ----------------------------
    prediction = predict_future(counts)

    # ----------------------------
    # Display Info
    # ----------------------------
    cv2.putText(frame, f"People: {people_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    if prediction:
        cv2.putText(frame, f"Predicted: {prediction}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

        # ALERT
        if prediction > 20:
            cv2.putText(frame, "⚠️ Overcrowding Risk!", (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

    cv2.imshow("Crowd Monitoring System", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ----------------------------
# 🔹 Release
# ----------------------------
cap.release()
cv2.destroyAllWindows()

# ----------------------------
# 📊 Plot Graph
# ----------------------------
plt.plot(counts, label="Actual Crowd")
if len(counts) > 5:
    pred = predict_future(counts)
    plt.scatter(len(counts)+5, pred, label="Predicted", marker='o')

plt.xlabel("Time")
plt.ylabel("People Count")
plt.legend()
plt.title("Crowd Prediction")
plt.show()