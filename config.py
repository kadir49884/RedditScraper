"""Reddit bot konfigürasyon dosyası."""


class Config:
    """Reddit bot konfigürasyon sınıfı."""
    
    USER_AGENT = "PetBot/1.0"
    
    # Yorum metni (bu metin yorum olarak yazılacak)
    COMMENT_TEXT = "Çok tatlı! 😍"
    
    # Evcil hayvan subredditleri
    PET_SUBREDDITS = [
        "aww",
        "cats",
        "dogs",
        "puppies",
        "kittens",
        "rarepuppers",
        "turkey",  # Türkiye subreddit'i (bazen evcil hayvan gönderileri olur)
        "turkeyjerky"  # Türkçe içerik olabilir
    ]

