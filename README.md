##FIRST WAY##

--

1️⃣ Camera detected correctly

bash
mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 640x480 -f 20" -o "output_http.so -p 8080 -w ./www"

url: http://192.168.29.19:8080/?action=stream
