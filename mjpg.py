import cv2
import mediapipe as mp
import time
from flask import Flask, Response, render_template_string

app = Flask(__name__)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# URL of your webcam stream
STREAM_URL = "http://192.168.29.19:8080/?action=stream"

def generate_frames():
    # Capture the stream from the given URL
    cap = cv2.VideoCapture(STREAM_URL)
    
    while True:
        success, frame = cap.read()
        if not success:
            # Reconnect if the stream drops
            time.sleep(0.1)
            cap = cv2.VideoCapture(STREAM_URL)
            continue
            
        # Convert the BGR image to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame and find hands
        results = hands.process(rgb_frame)
        
        # Draw the hand annotations on the image
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
                )
                    
        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        
        # Yield the frame in byte format for the web stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    # Simple, responsive UI containing the video feed
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MediaPipe Hand Tracking Stream</title>
        <style>
            body { 
                margin: 0; 
                padding: 0; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                min-height: 100vh; 
                background-color: #121212; 
                color: #e0e0e0; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                flex-direction: column; 
            }
            h1 { 
                margin-top: 20px; 
                margin-bottom: 20px;
                text-align: center; 
                font-weight: 300;
                letter-spacing: 1px;
            }
            .video-container { 
                width: 90vw; 
                max-width: 800px; 
                aspect-ratio: 4/3; 
                border: 2px solid #333; 
                border-radius: 12px; 
                overflow: hidden; 
                box-shadow: 0 8px 30px rgba(0,0,0,0.6); 
                background-color: #000;
            }
            img { 
                width: 100%; 
                height: 100%; 
                object-fit: cover; 
            }
            .device-info {
                margin-top: 20px;
                font-size: 0.9em;
                color: #888;
            }
        </style>
    </head>
    <body>
        <h1>Live Hand Tracking Stream</h1>
        <div class="video-container">
            <img src="{{ url_for('video_feed') }}" alt="Video Stream">
        </div>
        <div class="device-info">
            Access this stream from any device on the same WiFi.
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Run the app on all available network interfaces (0.0.0.0) 
    # to make it accessible to other devices on the same WiFi network.
    print("Starting Flask streaming server...")
    print("To view from another device, find this computer's IP address (e.g., 192.168.x.x)")
    print("and go to http://<YOUR-IP>:5000 in your mobile or desktop browser.")
    app.run(host='0.0.0.0', port=5000, debug=False)
