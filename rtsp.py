import cv2
import mediapipe as mp
import time
from flask import Flask, Response, render_template_string

app = Flask(__name__)

STREAM_URL = "rtsp://192.168.29.19:8554/webcam"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_draw = mp.solutions.drawing_utils

def generate_frames():

    cap = cv2.VideoCapture(STREAM_URL, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    while True:

        cap.grab()
        success, frame = cap.read()

        if not success:
            cap.release()
            time.sleep(0.5)
            cap = cv2.VideoCapture(STREAM_URL, cv2.CAP_FFMPEG)
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():

    html = """
    <html>
    <body style="background:black;color:white;text-align:center;">
        <h1>Live Hand Tracking</h1>
        <img src="/video_feed" width="800">
    </body>
    </html>
    """

    return render_template_string(html)


@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
