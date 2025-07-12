#!/bin/bash
echo "🔁 Starting 9:16 loop live stream..."#!/bin/bash

echo "🔁 Starting 9:16 loop live stream..."

ffmpeg -re -stream_loop -1 -i live1.mp4 \
-c:v libx264 -preset veryfast -maxrate 3000k -bufsize 6000k \
-vf "scale=1080:1920" \
-c:a aac -b:a 128k -ar 44100 \
-f flv "rtmp://a.rtmp.youtube.com/live2/$STREAM_KEY"
chmod +x loop.sh
./loop.sh
