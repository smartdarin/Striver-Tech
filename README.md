# 🚀 AI Crowd Intelligence System

## 📌 Overview

The **AI Crowd Intelligence System** is a real-time crowd monitoring and analysis platform that uses computer vision and machine learning to estimate crowd density, detect risk levels, and trigger emergency response actions.

This system is designed to prevent overcrowding incidents, manage large gatherings efficiently, and support safety teams with intelligent insights.

---

## 🎯 Key Features

### 🎥 Real-Time Crowd Monitoring

* Processes video input using OpenCV
* Generates heatmaps to visualize crowd density
* Divides area into zones for localized analysis

### 👥 Crowd Estimation

* Estimates number of people based on occupancy detection
* Calculates dynamic crowd capacity based on available space

### 🧠 AI-Based Intelligence

* Uses Linear Regression for short-term crowd prediction
* Performs trend analysis (increase/decrease)
* Detects instability and sudden fluctuations

### ⚠️ Risk Detection System

* Classifies crowd into:

  * 🟢 Safe
  * 🟡 Moderate
  * 🟠 High
  * 🔴 Critical
* Detects overcrowding and unsafe conditions

### 🚑 Emergency Response System

* Simulates real-world alert mechanisms:

  * 🚓 Police Control Room
  * 🚑 Emergency Medical Services
  * 🏥 Nearby Hospitals
* Triggers preventive or critical alerts automatically

### 📊 Interactive Dashboard (Streamlit)

* Live crowd trend visualization
* Smoothed graph for better insights
* Real-time stats:

  * Current Crowd
  * Average Crowd
  * Peak Crowd
* AI-based decision insights

---

## 🏗️ System Architecture

```
Video Input → OpenCV Processing → Density Estimation → AI Analysis → CSV Storage → Streamlit Dashboard
```

---

## 🛠️ Technologies Used

* **Python**
* **OpenCV** – Image processing & heatmaps
* **NumPy** – Numerical computations
* **Pandas** – Data handling
* **Scikit-learn** – Linear Regression (AI prediction)
* **Matplotlib** – Graph visualization
* **Streamlit** – Dashboard UI

---

## 📂 Project Structure

```
📁 Project Folder
│
├── main1.py              # Main AI crowd processing system
├── dashboard.py         # Streamlit dashboard
├── crowd_data.csv       # Generated data file
├── video.mp4            # Input video file
├── yolov8n.pt (optional) # Future AI upgrade
```

---

## ▶️ How to Run

### Step 1: Install Dependencies

```bash
pip install opencv-python numpy pandas matplotlib scikit-learn streamlit
```

### Step 2: Run Main System

```bash
python main1.py
```

* Press **Q** to stop safely
* CSV will be saved automatically

---

### Step 3: Run Dashboard

```bash
streamlit run dashboard.py
```

---

## 📊 Output

* Real-time crowd visualization
* AI-based crowd insights
* Risk level classification
* Emergency response simulation

---

## 🧠 AI Logic Explained

* **Crowd Detection** → Based on pixel density & edge detection
* **Prediction** → Linear Regression predicts future crowd
* **Trend Analysis** → Detects surge, drop, or stability
* **Decision Engine** → Triggers alerts based on thresholds

---

## 🌍 Applications

* 🎉 Public Events & Festivals
* ✈️ Airports & Railway Stations
* 🏟️ Stadiums
* 🕌 Pilgrimage Sites
* 🏙️ Smart Cities

---

## 🚀 Future Enhancements

* 🔥 YOLOv8-based real human detection
* 📱 SMS/Notification alert system
* 📍 GPS-based location tracking
* ☁️ Cloud deployment
* 📡 IoT integration with CCTV systems

---

## 🏆 Conclusion

This system demonstrates how **AI + Computer Vision** can be used to:

* Enhance public safety
* Prevent crowd disasters
* Enable smart crowd management

---

## 👨‍💻 Developed By
Striver-Tech


---

⭐ *“From detection to decision — making crowds safer with AI.”*
