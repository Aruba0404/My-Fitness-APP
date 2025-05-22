# 🏋️‍♂️ AI Fitness Trainer - Real-Time Exercise Feedback System

This project is a real-time fitness form correction app that uses **MediaPipe**, **OpenCV**, and **Streamlit** to detect your posture during **Squats**, **Push-ups**, and **Planks**, and provide **visual** and **voice feedback** for better exercise form and injury prevention.

> 🎯 Final Year Project - BS Data Science (2025)

---

## 💡 Features

- 🧍‍♂️ Pose detection using **MediaPipe**
- 📐 Real-time angle analysis and rep counting
- ✅ Form correction feedback (visual + audio)
- ⏱️ Plank duration timer
- 🎙️ Friendly voice guidance (optional)
- 📊 Correct vs Incorrect rep tracking
- 🔴 Live webcam mode + 📁 Video upload mode
- 💻 Clean, interactive Streamlit UI

---

## 📂 Folder Structure

├── app.py
├── pose_estimation/
│ ├── detect_pose.py
│ └── draw_landmarks.py
├── posture_analysis/
│ └── evaluate_posture.py
├── logic/
│ ├── angle_utils.py
│ ├── rep_counter.py
├── utils/
├ └── text_to_speech.py
├ └── timer_utils.py
├── requirements.txt
├── README.md


---

## 🚀 How to Run the App

### 🔧 Step 1: Clone the Repo

```bash
git clone https://github.com/https://github.com/Aruba0404


### 📦 Step 2: Install Dependencies
### Use pip to install the required packages:

pip install -r requirements.txt

# ▶️ Step 3: Run the App

streamlit run app.py

#########################################################################################

### 🛠️ Tech Stack
Python 3.8+

Streamlit – UI and interaction

OpenCV – Video and image processing

MediaPipe – Pose estimation

pyttsx3 – Text-to-speech engine


# 🎓 Authors
ARUBA BIBI, ZAINAB BIBI

Supervised by: [DR M.Ibrahim]

#########################################################################################