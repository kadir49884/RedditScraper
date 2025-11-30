"""Reddit evcil hayvan botu - API olmadan gönderileri bulur ve gösterir."""
import requests
import time
from datetime import datetime, timedelta
from config import Config


class RedditPetBot:
    """Reddit evcil hayvan gönderilerini bulan bot."""
    
    def __init__(self):
        """Bot'u başlat."""
        self.headers = {'User-Agent': Config.USER_AGENT}
        self.seen_posts = set()
    
    def is_within_24_hours(self, created_utc):
        """Gönderi son 24 saat içinde mi kontrol et."""
        post_time = datetime.fromtimestamp(created_utc)
        now = datetime.now()
        time_diff = now - post_time
        return time_diff <= timedelta(hours=24)
    
    def get_pet_posts(self, subreddit_name, limit=100):
        """Bir subreddit'ten son 24 saatteki en popüler gönderileri getir."""
        # Son 24 saatteki en popüler gönderiler için top endpoint kullan
        url = f"https://www.reddit.com/r/{subreddit_name}/top.json?t=day&limit={limit}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            posts = []
            for post_data in data.get('data', {}).get('children', []):
                post = post_data.get('data', {})
                post_id = post.get('id')
                created_utc = post.get('created_utc', 0)
                score = post.get('score', 0)
                
                if post_id and post_id not in self.seen_posts:
                    # Son 24 saat içindeki gönderileri kontrol et
                    if self.is_within_24_hours(created_utc):
                        posts.append({
                            'id': post_id,
                            'title': post.get('title', ''),
                            'url': f"https://reddit.com{post.get('permalink', '')}",
                            'score': score,
                            'subreddit': subreddit_name,
                            'created_utc': created_utc
                        })
                        self.seen_posts.add(post_id)
            
            # Score'a göre sırala (en yüksekten en düşüğe)
            posts.sort(key=lambda x: x['score'], reverse=True)
            
            return posts
            
        except Exception as e:
            print(f"❌ Subreddit '{subreddit_name}' için hata: {e}")
            return []
    
    def display_posts(self, posts):
        """Gönderileri ekrana yazdır."""
        for post in posts:
            print(f"\n📌 r/{post['subreddit']}")
            print(f"   {post['title'][:70]}")
            print(f"   ⬆️ {post['score']} upvote | 🔗 {post['url']}")
    
    def run(self, delay_seconds=300):
        """Bot'u çalıştır."""
        print("🤖 Reddit Pet Bot başlatılıyor...")
        print("🔥 Son 24 saatteki en popüler evcil hayvan gönderileri aranıyor...\n")
        
        while True:
            try:
                all_posts = []
                
                for subreddit_name in Config.PET_SUBREDDITS:
                    posts = self.get_pet_posts(subreddit_name, limit=25)
                    all_posts.extend(posts)
                    time.sleep(1)
                
                # Tüm gönderileri score'a göre sırala
                all_posts.sort(key=lambda x: x['score'], reverse=True)
                
                if all_posts:
                    print(f"\n🐾 {len(all_posts)} popüler evcil hayvan gönderisi bulundu:\n")
                    self.display_posts(all_posts[:10])
                else:
                    print("⚠️ Son 24 saatte gönderi bulunamadı.")
                
                print(f"\n⏳ {delay_seconds} saniye bekleniyor...\n")
                time.sleep(delay_seconds)
                
            except KeyboardInterrupt:
                print("\n🛑 Bot durduruldu.")
                break
            except Exception as e:
                print(f"❌ Hata: {e}")
                time.sleep(delay_seconds)


if __name__ == "__main__":
    bot = RedditPetBot()
    bot.run(delay_seconds=300)

