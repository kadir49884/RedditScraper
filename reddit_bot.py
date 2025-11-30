"""Reddit evcil hayvan botu - API olmadan gönderileri bulur ve gösterir."""
import requests
import time
from config import Config


class RedditPetBot:
    """Reddit evcil hayvan gönderilerini bulan bot."""
    
    def __init__(self):
        """Bot'u başlat."""
        self.headers = {'User-Agent': Config.USER_AGENT}
        self.seen_posts = set()
        self.turkish_chars = set('ğüşıöçĞÜŞİÖÇ')
    
    def is_turkish(self, text):
        """Metnin Türkçe olup olmadığını kontrol et."""
        if not text:
            return False
        
        text_lower = text.lower()
        
        # Türkçe karakter kontrolü
        has_turkish_chars = any(char in self.turkish_chars for char in text)
        
        # Yaygın Türkçe kelimeler kontrolü
        turkish_words = ['kedi', 'köpek', 'küçük', 'tatlı', 'sevimli', 'hayvan', 
                        'pati', 'kuyruk', 'göz', 'sevgi', 'oyun', 'mama', 'su']
        has_turkish_words = any(word in text_lower for word in turkish_words)
        
        return has_turkish_chars or has_turkish_words
    
    def get_pet_posts(self, subreddit_name, limit=10):
        """Bir subreddit'ten gönderileri getir."""
        url = f"https://www.reddit.com/r/{subreddit_name}/hot.json?limit={limit}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            posts = []
            for post_data in data.get('data', {}).get('children', []):
                post = post_data.get('data', {})
                post_id = post.get('id')
                title = post.get('title', '')
                
                if post_id and post_id not in self.seen_posts:
                    # Sadece Türkçe gönderileri ekle
                    if self.is_turkish(title):
                        posts.append({
                            'id': post_id,
                            'title': title,
                            'url': f"https://reddit.com{post.get('permalink', '')}",
                            'score': post.get('score', 0),
                            'subreddit': subreddit_name
                        })
                        self.seen_posts.add(post_id)
            
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
        print("🇹🇷 Sadece Türkçe gönderiler aranıyor...\n")
        
        while True:
            try:
                all_posts = []
                
                for subreddit_name in Config.PET_SUBREDDITS:
                    posts = self.get_pet_posts(subreddit_name, limit=20)
                    all_posts.extend(posts)
                    time.sleep(1)
                
                if all_posts:
                    print(f"\n🐾 {len(all_posts)} Türkçe evcil hayvan gönderisi bulundu:\n")
                    self.display_posts(all_posts[:10])
                else:
                    print("⚠️ Türkçe gönderi bulunamadı.")
                
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

