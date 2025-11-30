"""Telefon için basit web arayüzü - Gönderilere tek tıkla yorum yap."""
from flask import Flask, render_template_string, jsonify
from reddit_bot import RedditPetBot
from config import Config
import threading
import time
import os

app = Flask(__name__)
bot = RedditPetBot()
posts_cache = []
last_update = 0

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reddit Pet Bot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            padding: 10px;
        }
        .header {
            background: #ff4500;
            color: white;
            padding: 15px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .post {
            background: white;
            margin: 10px 0;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .post-title {
            font-size: 16px;
            margin-bottom: 10px;
            color: #333;
        }
        .post-info {
            font-size: 12px;
            color: #666;
            margin-bottom: 10px;
        }
        .comment-btn {
            background: #ff4500;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 5px;
            font-size: 16px;
            width: 100%;
            cursor: pointer;
            margin-top: 10px;
        }
        .comment-btn:active {
            background: #cc3700;
        }
        .refresh-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            width: 100%;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .no-posts {
            text-align: center;
            padding: 40px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🐾 Reddit Pet Bot</h1>
        <p>Türkçe Evcil Hayvan Gönderileri</p>
    </div>
    
    <button class="refresh-btn" onclick="location.reload()">🔄 Yenile</button>
    
    <div id="posts">
        {% if posts %}
            {% for post in posts %}
            <div class="post">
                <div class="post-title">{{ post.title }}</div>
                <div class="post-info">
                    r/{{ post.subreddit }} • ⬆️ {{ post.score }} upvote
                </div>
                <button class="comment-btn" onclick="commentPost('{{ post.url }}')">
                    💬 Yorum Yap
                </button>
            </div>
            {% endfor %}
        {% else %}
            <div class="no-posts">
                <p>Henüz gönderi bulunamadı.</p>
                <p>Biraz bekleyip yenileyin.</p>
            </div>
        {% endif %}
    </div>
    
    <script>
        const commentText = "{{ comment_text }}";
        
        function commentPost(url) {
            // Metni panoya kopyala
            navigator.clipboard.writeText(commentText).then(function() {
                alert("✅ Yorum metni kopyalandı! Reddit'e gidiyor...");
                // Reddit yorum sayfasına git
                window.open(url, '_blank');
            }).catch(function() {
                // Eski tarayıcılar için alternatif
                const textarea = document.createElement('textarea');
                textarea.value = commentText;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                alert("✅ Yorum metni kopyalandı! Reddit'e gidiyor...");
                window.open(url, '_blank');
            });
        }
        
        // Her 30 saniyede bir otomatik yenile
        setInterval(function() {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
"""


def update_posts():
    """Gönderileri güncelle."""
    global posts_cache, last_update
    
    while True:
        try:
            all_posts = []
            for subreddit_name in Config.PET_SUBREDDITS:
                posts = bot.get_pet_posts(subreddit_name, limit=20)
                all_posts.extend(posts)
                time.sleep(1)
            
            posts_cache = all_posts[:20]  # En fazla 20 gönderi
            last_update = time.time()
            print(f"✅ {len(posts_cache)} gönderi güncellendi")
            
        except Exception as e:
            print(f"❌ Güncelleme hatası: {e}")
        
        time.sleep(300)  # 5 dakikada bir güncelle


@app.route('/')
def index():
    """Ana sayfa."""
    return render_template_string(
        HTML_TEMPLATE, 
        posts=posts_cache,
        comment_text=Config.COMMENT_TEXT
    )


@app.route('/api/posts')
def api_posts():
    """API endpoint - JSON formatında gönderiler."""
    return jsonify(posts_cache)


if __name__ == '__main__':
    # Arka planda gönderi güncelleme thread'i başlat
    update_thread = threading.Thread(target=update_posts, daemon=True)
    update_thread.start()
    
    # Railway için port ayarı
    port = int(os.environ.get('PORT', 5000))
    
    print("🤖 Web uygulaması başlatılıyor...")
    print(f"🌐 Port: {port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)

