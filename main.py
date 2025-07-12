
import time
import requests
import subprocess
import os

STATUS_URL = os.getenv("STATUS_URL", "https://shorts-control.onrender.com/status")
STREAM_KEY = os.getenv("STREAM_KEY", "PASTE_YOUR_KEY")
VIDEO_PATH = "video.mp4"

def is_status_on():
    try:
        r = requests.get(STATUS_URL, timeout=5)
        return r.json().get("status") == "ON"
    except:
        return False

def start_stream():
    print("🎬 Mulai streaming loop...")
    command = [
        "ffmpeg", "-re", "-stream_loop", "-1", "-i", VIDEO_PATH,
        "-c:v", "libx264", "-preset", "veryfast", "-maxrate", "3000k",
        "-bufsize", "6000k", "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
        "-f", "flv", f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
    ]
    return subprocess.Popen(command)

if __name__ == "__main__":
    print("🔄 shorts-live aktif, monitoring status setiap 1 menit...")
    process = None
    while True:
        if is_status_on():
            if not process or process.poll() is not None:
                print("✅ Status ON → Mulai streaming...")
                process = start_stream()
            else:
                print("📶 Streaming masih berjalan...")
        else:
            if process:
                print("⛔ Status OFF → Stop streaming...")
                process.terminate()
                process = None
            else:
                print("🛑 Status masih OFF")
        time.sleep(60)
