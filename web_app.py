"""Telefon için basit web arayüzü - Gönderilere tek tıkla yorum yap."""
from flask import Flask, render_template_string, jsonify, request
from reddit_bot import RedditPetBot
from config import Config
from commented_posts import CommentedPostsManager
from comment_manager import CommentManager
import time
import os

app = Flask(__name__)
bot = RedditPetBot()
posts_manager = CommentedPostsManager()
comment_manager = CommentManager()
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
            background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
            color: white;
            border: none;
            padding: 14px 20px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 6px rgba(74, 144, 226, 0.3);
        }
        
        .comment-btn:active {
            transform: scale(0.98);
        }
        
        .post-actions {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        
        .post-actions button {
            flex: 1;
        }
        
        .remove-btn {
            background: linear-gradient(135deg, #ff4757 0%, #ee3742 100%);
            color: white;
            border: none;
            padding: 14px 20px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
            box-shadow: 0 4px 6px rgba(255, 71, 87, 0.3);
        }
        
        .remove-btn:active {
            transform: scale(0.98);
        }
        
        .searching {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .searching-text {
            color: #667eea;
            font-size: 16px;
            font-weight: 600;
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
        
        .searching {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .searching-text {
            color: #667eea;
            font-size: 16px;
            font-weight: 600;
        }
        
        .remove-btn {
            background: #ff4757;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 10px;
            width: 100%;
            transition: transform 0.2s;
        }
        
        .remove-btn:active {
            transform: scale(0.98);
        }
        
        .post-actions {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        
        .post-actions button {
            flex: 1;
        }
        
        @media (max-width: 768px) {
            body {
                padding: 15px;
            }
            
            .container {
                max-width: 100%;
            }
            
            .header {
                padding: 20px 15px;
            }
            
            .header h1 {
                font-size: 24px;
            }
            
            .header p {
                font-size: 13px;
            }
            
            .post {
                padding: 15px;
            }
            
            .post-title {
                font-size: 16px;
                line-height: 1.3;
            }
            
            .post-info {
                flex-wrap: wrap;
                gap: 8px;
                font-size: 12px;
            }
            
            .post-actions {
                gap: 8px;
            }
            
            .comment-btn,
            .remove-btn {
                padding: 12px 16px;
                font-size: 15px;
            }
            
            .stats {
                padding: 12px 15px;
                font-size: 13px;
            }
            
            .refresh-btn {
                padding: 12px;
                font-size: 15px;
            }
        }
        
        @media (max-width: 480px) {
            body {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 22px;
            }
            
            .post-title {
                font-size: 15px;
            }
            
            .comment-btn,
            .remove-btn {
                padding: 10px 14px;
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐾 Reddit Pet Bot</h1>
            <p>Son 24 Saatteki En Popüler Gönderiler</p>
        </div>
        
        {% if posts %}
        <div class="stats">
            <span class="stats-text">📊 Toplam Gönderi</span>
            <span class="stats-count">{{ posts|length }}</span>
        </div>
        {% endif %}
        
        <button class="refresh-btn" onclick="refreshPosts()">
            🔄 Yenile
        </button>
        
        <div id="searching-status" style="display: none;">
            <div class="searching">
                <div class="searching-text">🔍 Gönderiler aranıyor...</div>
            </div>
        </div>
        
        <div id="posts">
            {% if posts %}
                {% for post in posts %}
                <div class="post" data-post-id="{{ post.id }}">
                    <div class="post-title">{{ post.title }}</div>
                    <div class="post-info">
                        <span>📌 r/{{ post.subreddit }}</span>
                        <span>⬆️ {{ post.score }}</span>
                        <span>💬 {{ post.num_comments|default(0) }}</span>
                    </div>
                    <div class="post-actions">
                        <button class="comment-btn" data-comment-id="{{ post.comment_id }}" onclick="commentPost('{{ post.url }}', '{{ post.id }}', '{{ post.comment_id }}')">
                            💬 Yorum Yap
                        </button>
                        <button class="remove-btn" onclick="removePost('{{ post.id }}')">
                            ❌ Kaldır
                        </button>
                    </div>
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
        const commentTexts = {{ comment_texts_map|tojson }};
        
        function refreshPosts() {
            const statusDiv = document.getElementById('searching-status');
            const postsDiv = document.getElementById('posts');
            
            // Arama durumunu göster
            statusDiv.style.display = 'block';
            postsDiv.innerHTML = '';
            
            // Sunucuya yenileme isteği gönder
            fetch('/api/refresh', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            }).then(function() {
                // Sayfayı yenile
                setTimeout(function() {
                    location.reload();
                }, 1000);
            });
        }
        
        function removePost(postId) {
            const postElement = document.querySelector(`[data-post-id="${postId}"]`);
            
            if (postElement) {
                // Sunucuya kaldırma isteği gönder
                fetch('/api/remove', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({post_id: postId})
                });
                
                // Gönderiyi animasyonlu şekilde kaldır
                postElement.style.transition = 'opacity 0.3s, transform 0.3s';
                postElement.style.opacity = '0';
                postElement.style.transform = 'translateX(-20px)';
                
                setTimeout(function() {
                    postElement.remove();
                    // Eğer gönderi kalmadıysa sayfayı yenile
                    if (document.querySelectorAll('.post').length === 0) {
                        location.reload();
                    }
                }, 300);
            }
        }
        
        function commentPost(url, postId, commentId) {
            const btn = event.target;
            const originalText = btn.innerHTML;
            const postElement = btn.closest('.post');
            const commentText = commentTexts[commentId] || '';
            
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
        
    </script>
</body>
</html>
"""




@app.route('/')
def index():
    """Ana sayfa."""
    # Yorum yapılan gönderileri filtrele
    filtered_posts = posts_manager.filter_commented(posts_cache)
    
    # En az 5 gönderi göster (eğer yoksa tümünü göster)
    display_posts = filtered_posts[:50] if len(filtered_posts) >= 5 else filtered_posts
    
    # Her gönderi için rastgele yorum metni seç
    posts_with_comments = []
    comment_texts_map = {}
    for i, post in enumerate(display_posts):
        post_copy = post.copy()
        comment_text = comment_manager.get_random_comment()
        post_copy['comment_id'] = f"comment_{i}"
        comment_texts_map[f"comment_{i}"] = comment_text
        posts_with_comments.append(post_copy)
    
    return render_template_string(
        HTML_TEMPLATE, 
        posts=posts_with_comments,
        comment_texts_map=comment_texts_map
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


@app.route('/api/refresh', methods=['POST'])
def refresh_posts():
    """Gönderileri manuel olarak yenile."""
    global posts_cache
    
    try:
        # seen_posts'u temizle (yeni gönderiler bulabilmek için)
        bot.seen_posts.clear()
        
        # Gönderileri hemen güncelle
        all_posts = []
        for subreddit_name in Config.PET_SUBREDDITS:
            posts = bot.get_pet_posts(subreddit_name, limit=100)
            all_posts.extend(posts)
            time.sleep(0.3)  # Daha hızlı tarama
        
        # Önce son 1 saat içindekileri, sonra diğerlerini sırala
        # Her grup içinde etkileşim skoruna göre sırala
        all_posts.sort(key=lambda x: (not x.get('is_recent', False), -x.get('engagement_score', x.get('score', 0))))
        
        # Yorum yapılan gönderileri filtrele
        filtered_posts = posts_manager.filter_commented(all_posts)
        # En az 5 gönderi garantisi için daha fazla gönderi göster
        posts_cache = filtered_posts[:50]  # Daha fazla gönderi göster
        
        return jsonify({'status': 'success', 'count': len(posts_cache)})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/remove', methods=['POST'])
def remove_post():
    """Gönderiyi listeden kaldır."""
    try:
        data = request.get_json()
        post_id = data.get('post_id')
        
        if post_id:
            # Yorum yapılanlar listesine ekle (böylece bir daha gösterilmez)
            posts_manager.add_commented(post_id)
            
            # Cache'den de kaldır
            global posts_cache
            posts_cache = [p for p in posts_cache if p.get('id') != post_id]
            
            return jsonify({'status': 'success', 'message': 'Gönderi kaldırıldı'})
        else:
            return jsonify({'status': 'error', 'message': 'Post ID gerekli'}), 400
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    # Railway için port ayarı
    port = int(os.environ.get('PORT', 5000))
    
    print("🤖 Web uygulaması başlatılıyor...")
    print("📌 Sadece manuel yenileme ile tarama yapılacak")
    print(f"🌐 Port: {port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)

