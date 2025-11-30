"""Yorum metinlerini rastgele seçen ve son kullanılanları takip eden modül."""
import random
from config import Config


class CommentManager:
    """Yorum metinlerini yönetir."""
    
    def __init__(self):
        """Yöneticiyi başlat."""
        self.comment_texts = Config.COMMENT_TEXTS
        self.recent_comments = []  # Son kullanılan metinler (max 5)
        self.last_comment = None  # Son kullanılan metin
    
    def get_random_comment(self):
        """Rastgele bir yorum metni seç (son 5'ten farklı ve üst üste aynı olmayan)."""
        available_texts = self.comment_texts.copy()
        
        # Son kullanılan metni kaldır (üst üste aynı olmasın)
        if self.last_comment and self.last_comment in available_texts:
            available_texts.remove(self.last_comment)
        
        # Son 5 metinden farklı olanları seç
        if len(self.recent_comments) >= 5:
            for recent in self.recent_comments:
                if recent in available_texts:
                    available_texts.remove(recent)
        
        # Eğer tüm metinler kullanıldıysa, sadece son metni hariç tut
        if not available_texts:
            available_texts = [text for text in self.comment_texts if text != self.last_comment]
        
        # Rastgele seç
        selected = random.choice(available_texts)
        
        # Son kullanılanları güncelle
        self.last_comment = selected
        self.recent_comments.append(selected)
        
        # Son 5'i tut (daha eski olanları sil)
        if len(self.recent_comments) > 5:
            self.recent_comments = self.recent_comments[-5:]
        
        return selected

