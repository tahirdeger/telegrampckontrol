"""
Telegram PC Controller - Yapılandırma Dosyası
Güvenli versiyon (GitHub uyumlu): hassas veriler secret.json'dan okunur
"""

import platform
import json
import os
import sys

# ============================================
# GÜVENLİK AYARLARI (JSON ÜZERİNDEN)
# ============================================

def get_base_path():
    """Uygulamanın çalıştığı ana dizini döndürür (EXE uyumlu)"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def load_secrets():
    """secret.json dosyasından güvenli değişkenleri yükler."""
    secret_path = os.path.join(get_base_path(), "secret.json")

    # Eğer dosya yoksa örnek bir şablon oluştur
    if not os.path.exists(secret_path):
        default_secret = {
            "BOT_TOKEN": "BURAYA_BOT_TOKEN_YAZIN",
            "AUTHORIZED_CHAT_ID": 0
        }
        with open(secret_path, "w", encoding="utf-8") as f:
            json.dump(default_secret, f, indent=4)
        print("⚠️ secret.json dosyası oluşturuldu. Lütfen API token ve chat ID ekleyin!")
        return default_secret

    try:
        with open(secret_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not data.get("BOT_TOKEN") or not data.get("AUTHORIZED_CHAT_ID"):
                raise ValueError("Eksik veri")
            return data
    except Exception as e:
        print(f"❌ secret.json okunamadı: {e}")
        return {"BOT_TOKEN": None, "AUTHORIZED_CHAT_ID": 0}


# Değerleri yükle
_secrets = load_secrets()
BOT_TOKEN = _secrets.get("BOT_TOKEN")
AUTHORIZED_CHAT_ID = _secrets.get("AUTHORIZED_CHAT_ID")
# ============================================
# UYGULAMA AYARLARI
# ============================================

# Bot açıklama mesajı
WELCOME_MESSAGE = """
🖥️ *PC Kontrol Botu Aktif*

Kullanılabilir komutlar:
/pcdurum - Sistem durumu
/ekrangoruntu - Ekran görüntüsü
/kameragoruntu - Webcam görüntüsü
/oturumkapat - Oturumu kapat
/pckapat - Bilgisayarı kapat

⚠️ Güvenlik: Sadece yetkili kullanıcı komut gönderebilir.
"""

# Loglama ayarı
ENABLE_LOGGING = True

# ============================================
# SİSTEM KOMUTLARI (İşletim Sistemine Göre)
# ============================================
import platform

OS_TYPE = platform.system()  # 'Windows', 'Linux', 'Darwin' (macOS)

# Sistem komutları (otomatik seçilir)
if OS_TYPE == "Windows":
    SHUTDOWN_CMD = "shutdown /s /t 10"  # 10 saniye içinde kapanır
    LOGOUT_CMD = "shutdown /l"
elif OS_TYPE == "Linux":
    SHUTDOWN_CMD = "shutdown -h +1"  # 1 dakika içinde kapanır
    LOGOUT_CMD = "pkill -KILL -u $USER"
elif OS_TYPE == "Darwin":  # macOS
    SHUTDOWN_CMD = "sudo shutdown -h +1"
    LOGOUT_CMD = "osascript -e 'tell application \"System Events\" to log out'"
else:
    SHUTDOWN_CMD = None
    LOGOUT_CMD = None

# ============================================
# EKRAN GÖRÜNTÜSÜ AYARLARI
# ============================================

# Geçici dosya yolu
SCREENSHOT_PATH = "temp_screenshot.png"

# Görüntü kalitesi (1-100 arası, yüksek = daha iyi kalite)
SCREENSHOT_QUALITY = 85


# ============================================
# HATA MESAJLARI
# ============================================

ERROR_MESSAGES = {
    "unauthorized": "⛔ Yetkisiz erişim! Bu bot sadece sahibi tarafından kullanılabilir.",
    "config_error": "❌ Yapılandırma hatası: BOT_TOKEN ve AUTHORIZED_CHAT_ID ayarlanmalı!",
    "command_failed": "❌ Komut çalıştırılamadı: {}",
    "unsupported_os": "❌ İşletim sisteminiz desteklenmiyor: {}",
}

# Otomatik başlatma
AUTOSTART_BOT = True
