
---

# Features

- Low latency streaming
- Real-time hand tracking
- Accessible on any device in the same WiFi network
- Auto reconnect if stream drops
- Clean Flask UI
- Scalable architecture

---

# Hardware Requirements

- Raspberry Pi Zero 2W
- USB Webcam
- MicroSD Card (16GB+ recommended)
- WiFi network
- Computer for MediaPipe processing

---

# Software Requirements

## Raspberry Pi

- Raspberry Pi OS (Bookworm recommended)
- GStreamer
- MediaMTX RTSP server

## Computer

- Python 3
- OpenCV
- MediaPipe
- Flask

---

# Step 1 — Update Raspberry Pi

```bash
sudo apt update
sudo apt upgrade -y
```

# Step 2 — Install Required Packages

```bash
sudo apt install -y \
gstreamer1.0-tools \
gstreamer1.0-plugins-base \
gstreamer1.0-plugins-good \
gstreamer1.0-plugins-bad \
gstreamer1.0-plugins-ugly \
gstreamer1.0-libav \
gstreamer1.0-rtsp \
v4l-utils
```

# Start the RTSP server:

```bash
./mediamtx
```

# Step 5 — Start Camera Stream

-Open another terminal and run:

```bash
gst-launch-1.0 v4l2src device=/dev/video0 ! \
video/x-raw,format=YUY2,width=320,height=240,framerate=20/1 ! \
videoconvert ! \
x264enc tune=zerolatency bitrate=300 speed-preset=ultrafast key-int-max=15 ! \
rtspclientsink location=rtsp://127.0.0.1:8554/webcam
```

# Step 6 — Test the RTSP Stream

Open VLC Media Player
Go to Media → Open Network Stream
Enter:

```bash
rtsp://192.168.29.19:8554/webcam
```
If working correctly you will see the live video.

# Run rtsp.py from the repo:

```bash
python rtsp.py
```

