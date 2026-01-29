# 🚀 PC CONTROLLER - HIZLI BAŞLANGIÇ REHBERİ

Modern, güvenli ve kullanıcı dostu Telegram PC kontrol uygulaması.

Created by: TAHIR
---

## 📋 İÇİNDEKİLER

1. [Kurulum](#kurulum)
2. [İlk Çalıştırma](#ilk-çalıştırma)
3. [Telegram Komutları](#telegram-komutları)
4. [EXE Oluşturma](#exe-oluşturma)
5. [Özellikler](#özellikler)
6. [Sorun Giderme](#sorun-giderme)

---

## 🔧 KURULUM

### Gerekli Dosyalar

Projeniz şu dosyalardan oluşmalı:

```
pc_controller/
│
├── main.py              # Ana program
├── gui.py               # Grafik arayüz
├── bot_handler.py       # Telegram bot yöneticisi
├── system_control.py    # Sistem kontrol fonksiyonları
├── config.py            # Yapılandırma dosyası
├── setup_wizard.py      # İlk kurulum sihirbazı
├── build_exe.py         # EXE oluşturma script'i
└── requirements.txt     # Gerekli kütüphaneler
```

### Python Kurulumu (Gerekirse)

Python 3.11.8 yüklü değilse:
1. [Python.org](https://www.python.org/downloads/) adresinden indirin
2. Kurulumda **"Add Python to PATH"** seçeneğini işaretleyin

### Kütüphaneleri Yükleyin

Komut satırını (CMD) açın ve şunu çalıştırın:

```bash
pip install -r requirements.txt
```

**Yüklenen kütüphaneler:**
- `python-telegram-bot` → Telegram bot API
- `Pillow` → Ekran görüntüsü işleme
- `psutil` → Sistem bilgileri
- `pystray` → Sistem tepsisi ikonu
- `pyinstaller` → EXE oluşturma

---

## 🎯 İLK ÇALIŞTIRMA

### Adım 1: Programı Başlatın

```bash
python main.py
```

### Adım 2: Kurulum Sihirbazı

Program ilk açıldığında **5 adımlı sihirbaz** karşınıza çıkacak:

#### **1. Hoşgeldiniz Ekranı**
- Programa genel bakış
- "İleri" butonuna tıklayın

#### **2. Telegram Bot Oluşturma**
1. Telegram'da [@BotFather](https://t.me/botfather)'ı açın
2. `/newbot` komutunu gönderin
3. Bot adı belirleyin (örn: "PC Kontrolcüm")
4. Kullanıcı adı belirleyin (örn: "mypc_controller_bot")
5. Size verilen **TOKEN**'ı kopyalayın
6. Sihirbazdaki alana yapıştırın

**Örnek Token:**
```
123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

#### **3. Chat ID Öğrenme**
1. Bot'unuza Telegram'dan mesaj gönderin (örn: "merhaba")
2. "Chat ID Öğrenme Sayfasını Aç" butonuna tıklayın
3. Açılan sayfada şunu arayın:
```json
"chat":{"id":123456789
```
4. `id` değerini (örn: `123456789`) kopyalayın
5. Sihirbazdaki alana yapıştırın

#### **4. Başlangıç Ayarları**

**Seçenek 1:** Windows başlangıcında otomatik başlat
- ✅ İşaretlerseniz: Windows açılışında program otomatik başlar

**Seçenek 2:** Bot otomatik başlat
- ✅ İşaretlerseniz: Program açılınca bot servisi otomatik başlar

**💡 Öneri:** Her ikisini de işaretleyin!

#### **5. Tamamlandı**
- "Bitir" butonuna tıklayın
- Program başlayacak ve sistem tepsisine küçülecek

---

## 📱 TELEGRAM KOMUTLARI

Bot'unuza şu komutları gönderebilirsiniz:

| Komut | Açıklama | Örnek Çıktı |
|-------|----------|-------------|
| `/start` | Hoşgeldin mesajı ve yardım | Kullanılabilir komutlar listesi |
| `/status` | Sistem durumu | CPU: 45%, RAM: 8.2/16 GB |
| `/screenshot` | Ekran görüntüsü | 📸 Ekran görüntüsü gönderir |
| `/logout` | Oturumu kapat | Kullanıcı oturumunu kapatır |
| `/shutdown` | Bilgisayarı kapat | 10 saniye içinde kapatır |

### Güvenlik

- ✅ Sadece **belirlediğiniz Chat ID** komut gönderebilir
- ✅ Başka kullanıcılar mesaj gönderemez
- ✅ Bot token'ınız şifreli saklanır

---

## 💻 EXE OLUŞTURMA

### Hızlı Yöntem

```bash
python build_exe.py
```

Bu script otomatik olarak:
1. ✅ Gereksinimleri kontrol eder
2. ✅ Eski derlemeleri temizler
3. ✅ İkon oluşturur
4. ✅ EXE dosyası derler
5. ✅ Config.py'yi kopyalar
6. ✅ README.txt oluşturur

### Manuel Yöntem

```bash
pyinstaller --onefile --windowed --name=PCController --icon=app_icon.ico main.py
```

**Parametreler:**
- `--onefile`: Tek bir EXE dosyası
- `--windowed`: Konsol penceresi gösterme
- `--name`: Dosya adı
- `--icon`: Program ikonu

### Sonuç

`dist/` klasöründe:
```
dist/
├── PCController.exe  (Ana program ~25MB)
├── config.py         (Yapılandırma)
└── README.txt        (Kullanım kılavuzu)
```

**⚠️ ÖNEMLİ:** EXE'yi taşırken `config.py`'yi de taşıyın!

---

## ✨ ÖZELLİKLER

### Mevcut Yetenekler

- ✅ **Sistem Durumu:** CPU, RAM, Disk kullanımı
- ✅ **Ekran Görüntüsü:** Anlık ekran fotoğrafı
- ✅ **Webcam Görüntüsü:** Anlık webcam fotoğrafı
- ✅ **Sohbet:** Bilgisayar ve telegram arası mesajlaşma
- ✅ **Güç Yönetimi:** Kapatma, oturum kapatma
- ✅ **GUI Arayüz:** Modern ve kullanıcı dostu
- ✅ **Sistem Tepsisi:** Arka planda sessizce çalışır
- ✅ **Otomatik Başlatma:** Windows açılışında başlar
- ✅ **Güvenlik:** Tek kullanıcı yetkilendirme

### Gelecek Özellikler (Modüler Yapı Sayesinde Kolay)

`system_control.py` dosyasına yeni fonksiyonlar ekleyerek:

```python
# Ses kontrolü
def set_volume(level):
    """Ses seviyesini ayarla (0-100)"""
    pass

# Uygulama açma
def open_application(app_name):
    """Belirtilen uygulamayı aç"""
    pass

# Dosya gönderme
def send_file(file_path):
    """Dosya gönder"""
    pass

# Webcam
def take_photo():
    """Webcam ile fotoğraf çek"""
    pass

# Klavye/Fare kontrolü
def send_keypress(key):
    """Klavye tuşuna bas"""
    pass
```

Sonra `bot_handler.py`'ye komut ekleyin:

```python
async def volume_command(self, update, context):
    level = int(context.args[0])
    self.system.set_volume(level)
    await update.message.reply_text(f"🔊 Ses: {level}")

# run() fonksiyonunda:
app.add_handler(CommandHandler("volume", self.volume_command))
```

---

## 🐛 SORUN GİDERME

### Program açılmıyor

**Hata:** `ModuleNotFoundError`
```bash
# Çözüm:
pip install -r requirements.txt
```

**Hata:** `config.py bulunamadı`
```bash
# Çözüm: config.py'nin main.py ile aynı klasörde olduğundan emin olun
```

### Bot çalışmıyor

**Sorun:** Bot mesajlara cevap vermiyor

**Çözümler:**
1. ✅ Ayarlar → Bot Token'ı kontrol edin
2. ✅ Ayarlar → Chat ID'yi kontrol edin
3. ✅ İnternet bağlantınızı kontrol edin
4. ✅ Bot'a önce mesaj gönderdiğinizden emin olun

### Komutlar çalışmıyor

**Sorun:** "Yetkisiz erişim" hatası

**Çözüm:**
- Chat ID'nizi yeniden öğrenin:
  1. Bot'a mesaj gönderin
  2. `https://api.telegram.org/bot<TOKEN>/getUpdates` sayfasını açın
  3. `"chat":{"id":` kısmındaki sayıyı bulun
  4. Ayarlar'dan güncelleyin

### Ekran görüntüsü çalışmıyor

**Sorun:** Ekran görüntüsü alınamıyor

**Çözüm:**
```bash
pip install --upgrade Pillow
```

### Windows Defender uyarısı

**Sorun:** EXE dosyası "zararlı" olarak işaretleniyor

**Çözüm:**
1. Bu normal bir durumdur (imzasız EXE)
2. "Daha fazla bilgi" → "Yine de çalıştır"
3. Windows Defender → İstisnalar'a ekleyin

### Otomatik başlatma çalışmıyor

**Sorun:** Windows başlangıcında açılmıyor

**Çözüm:**
1. Ayarlar → Başlangıç sekmesine gidin
2. "Windows başlangıcında otomatik başlat" seçeneğini işaretleyin
3. Veya manuel olarak:
   - `Win + R` → `shell:startup`
   - PCController.exe'nin kısayolunu buraya kopyalayın

---

## 💡 İPUÇLARI

### Performans

- 💚 **Hafif:** Boşta ~50MB RAM kullanır
- 💚 **Hızlı:** Komutlara anında cevap verir
- 💚 **Sessiz:** Arka planda hiç fark edilmez

### Güvenlik En İyi Uygulamaları

1. 🔒 Bot token'ınızı kimseyle paylaşmayın
2. 🔒 config.py dosyasını güvenli tutun
3. 🔒 Sadece güvendiğiniz Telegram hesabı ile kullanın
4. 🔒 Şüpheli aktivite görürseniz bot'u yeniden oluşturun

### Kullanım

- ✅ `/pcdurum` ile sistem durumunu kontrol edin
- ✅ `/ekrangoruntu` ile ekranı görün
- ✅ `/kameragoruntu` ile webcam fotografı alın
- ✅ `/pckapat` ile kapatın
- ✅  Tüm diğer yazdıklarınız bilgisayara mesaj olark gider

## 📞 DESTEK VE KATKI

### Katkıda Bulunun

Yeni özellikler eklemek için:

1. `system_control.py`'de fonksiyon yazın
2. `bot_handler.py`'de komut işleyici ekleyin
3. `config.py`'ye ayarları ekleyin
4. Test edin ve paylaşın!

### Örnek Katkı

```python
# system_control.py'ye:
def get_battery_status(self):
    battery = psutil.sensors_battery()
    return f"🔋 Pil: {battery.percent}%"

# bot_handler.py'ye:
async def battery_command(self, update, context):
    status = self.system.get_battery_status()
    await update.message.reply_text(status)

# run() fonksiyonuna:
app.add_handler(CommandHandler("battery", self.battery_command))
```

---

## 📄 LİSANS

Bu proje TAHIR tarafından eğitim amaçlı oluşturuldu. Kendi sorumluluğunuzda kullanın.

**Uyarı:** Başkalarının bilgisayarlarını izinsiz kontrol etmek yasalara aykırıdır!

---

**Hazırlayan:** TAHIR - "https://islematolyesi.odoo.com"
**Versiyon:** 1.0
**Son Güncelleme:** 2025

🎉 **Kurulumu tamamladınız! Artık bilgisayarınızı Telegram'dan kontrol edebilirsiniz!**