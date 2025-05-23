# 🚛 TruckDriverAlertSystem

TruckDriverAlertSystem is a computer vision-based safety solution that monitors a truck driver's eyes in real time using a webcam. If the system detects that the driver's eyes are closed for more than 4 seconds, it captures a photo and instantly sends an alert email — helping prevent accidents caused by drowsiness.

---

## 📌 Features

- 🚨 Real-time drowsiness detection
- 🧠 Uses MediaPipe FaceMesh for precise eye tracking
- 📷 Captures photo when drowsiness is detected
- ✉️ Sends alert email with the captured image
- 🖥️ Live webcam interface

---

## 🛠️ Required Libraries

Install the required Python libraries:

```bash
pip install opencv-python mediapipe
🐍 Imported Libraries
cv2 – OpenCV for video capture and image processing

mediapipe – Facial landmark detection for eye tracking

smtplib, email.mime – Email sending and photo attachment

time – (Imported but not used; can be removed)

⚙️ Email Configuration
Update these lines in the script with your email credentials:

python
Copy
Edit
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"  # Use Gmail App Password if 2FA enabled
receiver_email = "recipient_email@example.com"
