import os
import subprocess
import time
from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "🟢 Live streaming bot is running (Render.com)"

def run_flask():
    app.run(host="0.0.0.0", port=3000)

def start_stream():
    stream_key = os.getenv("STREAM_KEY")
    if not stream_key:
        print("❌ STREAM_KEY belum diset di Environment Variables.")
        return

    input_file = "live1.mp4"
    if not os.path.exists(input_file):
        print(f"❌ File {input_file} tidak ditemukan.")
        return

    print("🔁 Starting 9:16 loop live stream...")

    try:
        command = [
            "ffmpeg",
            "-re",
            "-stream_loop", "-1",
            "-i", input_file,
            "-vf", "scale=1080:1920",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-maxrate", "3000k",
            "-bufsize", "6000k",
            "-c:a", "aac",
            "-b:a", "128k",
            "-ar", "44100",
            "-f", "flv",
            f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"
        ]

        subprocess.run(command)
    except Exception as e:
        print(f"❌ Gagal jalankan ffmpeg: {e}")

if __name__ == "__main__":
    # Jalankan Flask server agar Render deteksi port
    Thread(target=run_flask).start()
    
    # Tunggu sebentar agar Flask stabil
    time.sleep(3)
    
    # Mulai loop streaming
    start_stream()
