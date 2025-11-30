"""Telefon için basit web arayüzü - Gönderilere tek tıkla yorum yap."""
from flask import Flask, render_template_string, jsonify, request
from reddit_bot import RedditPetBot
from config import Config
from commented_posts import CommentedPostsManager
import threading
import time
import os

app = Flask(__name__)
bot = RedditPetBot()
posts_manager = CommentedPostsManager()
posts_cache = []
last_update = 0

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="UTF-8">
    <title>Reddit Pet Bot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            padding: 25px 20px;
            text-align: center;
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            font-size: 28px;
            color: #333;
            margin-bottom: 8px;
            font-weight: 700;
        }
        
        .header p {
            color: #666;
            font-size: 14px;
        }
        
        .stats {
            background: white;
            padding: 15px 20px;
            border-radius: 12px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .stats-text {
            color: #666;
            font-size: 14px;
        }
        
        .stats-count {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
        }
        
        .refresh-btn {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border: none;
            padding: 14px;
            border-radius: 12px;
            width: 100%;
            margin-bottom: 20px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .refresh-btn:active {
            transform: translateY(2px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .post {
            background: white;
            margin-bottom: 16px;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .post:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .post-title {
            font-size: 17px;
            margin-bottom: 12px;
            color: #333;
            font-weight: 500;
            line-height: 1.4;
        }
        
        .post-info {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 13px;
            color: #888;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .post-info span {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .comment-btn {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            color: white;
            border: none;
            padding: 14px 20px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            width: 100%;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 6px rgba(238, 90, 111, 0.3);
        }
        
        .comment-btn:active {
            transform: scale(0.98);
        }
        
        .no-posts {
            background: white;
            text-align: center;
            padding: 60px 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .no-posts-icon {
            font-size: 64px;
            margin-bottom: 20px;
        }
        
        .no-posts h3 {
            color: #333;
            font-size: 20px;
            margin-bottom: 10px;
        }
        
        .no-posts p {
            color: #888;
            font-size: 14px;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: white;
            font-size: 18px;
        }
        
        @media (max-width: 480px) {
            body {
                padding: 15px;
            }
            
            .header h1 {
                font-size: 24px;
            }
            
            .post-title {
                font-size: 16px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐾 Reddit Pet Bot</h1>
            <p>Türkçe Evcil Hayvan Gönderileri</p>
        </div>
        
        {% if posts %}
        <div class="stats">
            <span class="stats-text">📊 Toplam Gönderi</span>
            <span class="stats-count">{{ posts|length }}</span>
        </div>
        {% endif %}
        
        <button class="refresh-btn" onclick="location.reload()">
            🔄 Yenile
        </button>
        
        <div id="posts">
            {% if posts %}
                {% for post in posts %}
                <div class="post">
                    <div class="post-title">{{ post.title }}</div>
                    <div class="post-info">
                        <span>📌 r/{{ post.subreddit }}</span>
                        <span>⬆️ {{ post.score }}</span>
                    </div>
                    <button class="comment-btn" onclick="commentPost('{{ post.url }}', '{{ post.id }}')">
                        💬 Yorum Yap
                    </button>
                </div>
                {% endfor %}
            {% else %}
                <div class="no-posts">
                    <div class="no-posts-icon">🔍</div>
                    <h3>Henüz gönderi bulunamadı</h3>
                    <p>Biraz bekleyip yenileyin</p>
                </div>
            {% endif %}
        </div>
    </div>
    
    <script>
        const commentText = "{{ comment_text }}";
        
        function commentPost(url, postId) {
            const btn = event.target;
            const originalText = btn.innerHTML;
            const postElement = btn.closest('.post');
            
            // Buton durumunu güncelle
            btn.innerHTML = "⏳ Kopyalanıyor...";
            btn.disabled = true;
            
            // Metni panoya kopyala
            navigator.clipboard.writeText(commentText).then(function() {
                btn.innerHTML = "✅ Kopyalandı!";
                
                // Sunucuya yorum yapıldığını bildir
                fetch('/api/commented', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({post_id: postId})
                });
                
                setTimeout(function() {
                    window.open(url, '_blank');
                    // Gönderiyi listeden kaldır
                    postElement.style.transition = 'opacity 0.3s';
                    postElement.style.opacity = '0';
                    setTimeout(function() {
                        postElement.remove();
                        // Eğer gönderi kalmadıysa sayfayı yenile
                        if (document.querySelectorAll('.post').length === 0) {
                            location.reload();
                        }
                    }, 300);
                }, 500);
            }).catch(function() {
                // Eski tarayıcılar için alternatif
                const textarea = document.createElement('textarea');
                textarea.value = commentText;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                
                btn.innerHTML = "✅ Kopyalandı!";
                
                // Sunucuya yorum yapıldığını bildir
                fetch('/api/commented', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({post_id: postId})
                });
                
                setTimeout(function() {
                    window.open(url, '_blank');
                    // Gönderiyi listeden kaldır
                    postElement.style.transition = 'opacity 0.3s';
                    postElement.style.opacity = '0';
                    setTimeout(function() {
                        postElement.remove();
                        // Eğer gönderi kalmadıysa sayfayı yenile
                        if (document.querySelectorAll('.post').length === 0) {
                            location.reload();
                        }
                    }, 300);
                }, 500);
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
            
            # Yorum yapılan gönderileri filtrele
            filtered_posts = posts_manager.filter_commented(all_posts)
            posts_cache = filtered_posts[:20]  # En fazla 20 gönderi
            last_update = time.time()
            print(f"✅ {len(posts_cache)} gönderi güncellendi (yorum yapılanlar filtrelendi)")
            
        except Exception as e:
            print(f"❌ Güncelleme hatası: {e}")
        
        time.sleep(300)  # 5 dakikada bir güncelle


@app.route('/')
def index():
    """Ana sayfa."""
    # Yorum yapılan gönderileri filtrele
    filtered_posts = posts_manager.filter_commented(posts_cache)
    
    return render_template_string(
        HTML_TEMPLATE, 
        posts=filtered_posts,
        comment_text=Config.COMMENT_TEXT
    )


@app.route('/api/posts')
def api_posts():
    """API endpoint - JSON formatında gönderiler."""
    return jsonify(posts_cache)


@app.route('/api/commented', methods=['POST'])
def mark_commented():
    """Yorum yapılan gönderiyi işaretle."""
    try:
        data = request.get_json()
        post_id = data.get('post_id')
        
        if post_id:
            posts_manager.add_commented(post_id)
            return jsonify({'status': 'success', 'message': 'Gönderi işaretlendi'})
        else:
            return jsonify({'status': 'error', 'message': 'Post ID gerekli'}), 400
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    # Arka planda gönderi güncelleme thread'i başlat
    update_thread = threading.Thread(target=update_posts, daemon=True)
    update_thread.start()
    
    # Railway için port ayarı
    port = int(os.environ.get('PORT', 5000))
    
    print("🤖 Web uygulaması başlatılıyor...")
    print(f"🌐 Port: {port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)

