"""Yorum yapılan gönderileri yöneten modül."""
import json
import os


class CommentedPostsManager:
    """Yorum yapılan gönderileri yönetir."""
    
    def __init__(self, filename='commented_posts.json'):
        """Yöneticiyi başlat."""
        self.filename = filename
        self.commented_ids = self._load_commented_ids()
    
    def _load_commented_ids(self):
        """Yorum yapılan gönderi ID'lerini dosyadan yükle."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get('commented_ids', []))
            except Exception as e:
                print(f"⚠️ Yorum dosyası okunamadı: {e}")
                return set()
        return set()
    
    def _save_commented_ids(self):
        """Yorum yapılan gönderi ID'lerini dosyaya kaydet."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump({'commented_ids': list(self.commented_ids)}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Yorum dosyası kaydedilemedi: {e}")
    
    def add_commented(self, post_id):
        """Yorum yapılan gönderi ID'sini ekle."""
        if post_id:
            self.commented_ids.add(post_id)
            self._save_commented_ids()
    
    def is_commented(self, post_id):
        """Gönderiye daha önce yorum yapılmış mı kontrol et."""
        return post_id in self.commented_ids
    
    def filter_commented(self, posts):
        """Yorum yapılmamış gönderileri filtrele."""
        return [post for post in posts if not self.is_commented(post.get('id'))]

