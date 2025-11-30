# Reddit Evcil Hayvan Botu 🐾

Reddit'teki Türkçe evcil hayvan gönderilerini bulan ve telefonunuzdan tek tıkla yorum yapmanızı sağlayan basit bir bot.

## Kurulum

1. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

## Kullanım

### Railway'de Çalıştırma (Önerilen - Her Yerden Erişim)

1. **Railway hesabı oluşturun:** https://railway.app
2. **Yeni proje oluşturun** ve GitHub repo'nuzu bağlayın
3. **Deploy edin** - Railway otomatik olarak:
   - `requirements.txt` dosyasını okur
   - `Procfile` ile uygulamayı başlatır
   - Port'u otomatik ayarlar

**Railway Deployment Adımları:**
```bash
# 1. Git repo'ya push edin
git add .
git commit -m "Railway deployment"
git push

# 2. Railway'de:
# - New Project > Deploy from GitHub repo
# - Repo'nuzu seçin
# - Otomatik deploy başlar
```

**Avantajlar:**
- ✅ Her yerden erişim (telefon, tablet, bilgisayar)
- ✅ Otomatik HTTPS
- ✅ Ücretsiz tier mevcut
- ✅ Otomatik yeniden başlatma

### Lokal Kullanım

```bash
python web_app.py
```

Sonra telefonunuzdan:
1. Bilgisayarınızla aynı WiFi ağına bağlanın
2. Tarayıcıdan şu adresi açın: `http://[BILGISAYAR_IP]:5000`
   - IP adresini öğrenmek için: Windows'ta `ipconfig`, Mac/Linux'ta `ifconfig`
   - Veya bu bilgisayardan: `http://localhost:5000`

**Nasıl Çalışır:**
- Gönderiler otomatik bulunur ve listelenir
- "💬 Yorum Yap" butonuna tıklayın
- Belirlediğiniz yorum metni otomatik kopyalanır
- Reddit açılır, yorum kutusuna yapıştırıp gönderin

### Konsol Versiyonu

```bash
python reddit_bot.py
```

## Ayarlar

### Yorum Metnini Değiştirme

`config.py` dosyasında `COMMENT_TEXT` değişkenini değiştirin:

```python
COMMENT_TEXT = "Çok tatlı! 😍"  # Buraya istediğiniz metni yazın
```

### Diğer Ayarlar

- `config.py`: Subreddit listesi ve yorum metni
- `web_app.py`: Web arayüzü ayarları
- `reddit_bot.py`: Konsol bot ayarları

## Lisans

MIT

