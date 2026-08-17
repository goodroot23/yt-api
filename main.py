from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/parse', methods=['GET'])
def parse():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
        
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        # 유튜브 봇 감지를 피하기 위해 iOS 및 MWEB 클라이언트로 위장
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'mweb']
            }
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            if not video_url:
                return jsonify({"status": "error", "message": "No video URL found"}), 400
            return jsonify({"status": "success", "url": video_url})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
