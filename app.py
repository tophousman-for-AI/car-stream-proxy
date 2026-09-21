from flask import Flask, redirect
import subprocess
import os

app = Flask(__name__)

@app.route('/stream/<video_id>')
def get_stream(video_id):
    yt_url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        # 加入 --extractor-args 模擬 iOS 客戶端，穿透 YouTube 機房封鎖
        cmd = [
            'yt-dlp',
            '--extractor-args', 'youtube:player_client=ios,web',
            '--no-check-certificates',
            '-g',
            yt_url
        ]
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        # 提煉第一行最高解析度 m3u8 直連
        m3u8_url = result.stdout.strip().split('\n')[0]
        return redirect(m3u8_url, code=302)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return f"串流提煉失敗: {error_msg}", 500
    except Exception as e:
        return f"系統錯誤: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
