What your terminal output means
1️⃣ Camera detected correctly

You ran:

mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 640x480 -f 20" -o "output_http.so -p 8080 -w ./www"

And it shows:

Using V4L2 device.: /dev/video0
Desired Resolution: 640 x 480
Frames Per Second.: 20

So your webcam is detected and working.

2️⃣ MJPG format not supported by camera

You see:

Could not obtain the requested pixelformat: MJPG
driver gave us: YUYV
Falling back to YUV mode

Meaning:

Your webcam does not support MJPEG hardware compression.

Instead it outputs:

YUYV

This forces the Pi to convert frames → higher CPU usage.

For a Pi Zero, we should fix this.

Fix (Best for Raspberry Pi Zero)

Run mjpg-streamer with YUYV option explicitly and reduce resolution.

Stop current stream with:

CTRL + C

Then run:

mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 320x240 -f 15 -y" -o "output_http.so -p 8080 -w ./www"

Explanation:

Option	Meaning
320x240	Lower resolution for Pi Zero
15 fps	Stable performance
-y	Use YUYV format

This will reduce CPU load massively.

About the other warnings

You see many lines like:

Error at Pan (relative)
Error at Tilt (relative)
Error at Focus

These happen because your webcam does not support those controls.

They are safe to ignore.

Now test the stream

Open browser on another device in the same Wi-Fi:

http://RASPBERRY_PI_IP:8080

Example:

http://192.168.1.42:8080

or directly:

http://192.168.1.42:8080/?action=stream

You should see the live webcam feed.
