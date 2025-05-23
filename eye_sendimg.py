import cv2
import mediapipe as mp
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# ==================== Email Setup ====================
def send_email_alert_with_photo(image_path):
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"  # Use Gmail App Password if 2FA enabled
receiver_email = "recipient_email@example.com"


    msg = MIMEMultipart()
    msg['Subject'] = "🚨 Drowsiness Alert"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    text = MIMEText("ALERT: Eyes were closed too long! See the attached photo.")
    msg.attach(text)

    try:
        with open(image_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-Disposition', 'attachment', filename="alert.jpg")
            msg.attach(img)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email with photo sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)

# ==================== MediaPipe Setup ====================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
cap = cv2.VideoCapture(0)

LEFT_EYE = [33, 159]  # top, bottom
RIGHT_EYE = [362, 386]

CLOSED_FRAMES = 0
THRESHOLD = 15
alert_sent = False

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    h, w, _ = frame.shape

    if results.multi_face_landmarks:
        mesh_points = results.multi_face_landmarks[0].landmark

        # Get eye coordinates
        l_top = int(mesh_points[LEFT_EYE[0]].y * h)
        l_bottom = int(mesh_points[LEFT_EYE[1]].y * h)
        r_top = int(mesh_points[RIGHT_EYE[0]].y * h)
        r_bottom = int(mesh_points[RIGHT_EYE[1]].y * h)

        # Eye closure logic
        left_ear = abs(l_top - l_bottom)
        right_ear = abs(r_top - r_bottom)

        if left_ear < 5 and right_ear < 5:
            CLOSED_FRAMES += 1
            cv2.putText(frame, "Eyes Closed", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        else:
            CLOSED_FRAMES = 0
            alert_sent = False

        if CLOSED_FRAMES > THRESHOLD and not alert_sent:
            print("Eyes closed too long. Capturing photo and sending alert...")

            # Save current frame
            img_path = "alert.jpg"
            cv2.imwrite(img_path, frame)

            # Send alert with photo
            send_email_alert_with_photo(img_path)
            alert_sent = True

    cv2.imshow("Eye Monitor", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
