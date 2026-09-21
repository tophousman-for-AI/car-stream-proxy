from flask import Flask, redirect
import subprocess
import os

app = Flask(__name__)

@app.route('/stream/<video_id>')
def get_stream(video_id):
    yt_url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        result = subprocess.run(
            ['yt-dlp', '-g', yt_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        # 提煉第一行最高解析度 m3u8，以 302 重導向塞回播放器
        m3u8_url = result.stdout.strip().split('\n')[0]
        return redirect(m3u8_url, code=302)
    except Exception as e:
        return f"串流提煉失敗: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
