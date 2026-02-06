"""
Telegram PC Controller - Ana Program (GUI Versiyonu)
Telegram üzerinden bilgisayarınızı uzaktan kontrol edin.

Kullanım:
    python main.py

Veya EXE olarak:
    pyinstaller --onefile --windowed --icon=icon.ico main.py
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox


def main():
    """Ana program başlatıcı"""
    
    # Windows başlangıcında çalışma dizinini düzelt (System32 sorunu ve Portable uyumluluk)
    if getattr(sys, 'frozen', False):
        # .exe olarak çalışıyorsa, .exe'nin olduğu dizin
        application_path = os.path.dirname(sys.executable)
    else:
        # .py olarak çalışıyorsa, main.py'nin olduğu dizin
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(application_path)
    if application_path not in sys.path:
        sys.path.insert(0, application_path)

    try:
        import config
        from setup_wizard import check_if_first_run, SetupWizard
        
        # İlk çalıştırma kontrolü
        if check_if_first_run():
            print("İlk çalıştırma tespit edildi. Kurulum sihirbazı başlatılıyor...")
            
            wizard = SetupWizard()
            completed = wizard.run()
            
            if not completed:
                print("Kurulum iptal edildi.")
                try:
                    # Kullanıcıya neden kapandığını bildiren bir mesaj göster
                    root = tk.Tk()
                    root.withdraw() # Ana pencereyi gösterme
                    messagebox.showinfo("Kurulum İptal Edildi", "Kurulum tamamlanmadığı için program kapatılıyor.")
                except:
                    pass # GUI hatası olursa sessizce devam et
                return
            
            # Config'i yeniden yükle
            import importlib
            importlib.reload(config)
            print("\n✅ Kurulum tamamlandı! GUI başlatılıyor...\n")
        
        # GUI modülünü import et
        from gui import PCControllerGUI
        from bot_handler import BotHandler
        
        print("🖥️ GUI penceresi açılıyor...")

        shots_dir = os.path.join(os.path.dirname(__file__), "shots")
        os.makedirs(shots_dir, exist_ok=True)
        
        # Bot handler oluştur
        bot_handler = BotHandler()
        
        # GUI oluştur ve çalıştır
        app = PCControllerGUI(bot_handler)
        
        # Otomatik başlatma kontrolü (sadece bir kere!)
        if getattr(config, 'AUTOSTART_BOT', False):
            if config.BOT_TOKEN and config.BOT_TOKEN != "BURAYA_BOT_TOKEN_YAZIN":
                if config.AUTHORIZED_CHAT_ID != 0:
                    print("🤖 Bot otomatik başlatılıyor...")
                    # Bot'u otomatik başlat (1 saniye sonra)
                    app.root.after(1000, lambda: app.start_bot() if not app.bot_running else None)
                    # Sistem tepsisine küçült (3 saniye sonra)
                    app.root.after(3000, app.minimize_to_tray)
        
        # GUI'yi çalıştır
        app.run()
        
    except ImportError as e:
        print(f"❌ Gerekli modül bulunamadı: {e}")
        print("\nEksik kütüphaneleri yükleyin:")
        print("pip install python-telegram-bot pillow psutil pystray")
        try:
            messagebox.showerror("Modül Hatası", f"Gerekli modül bulunamadı:\n{e}\n\nLütfen EXE'yi yeniden derleyin.")
        except:
            pass
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Kritik hata: {e}")
        print("\nHata detayları:")
        import traceback
        traceback.print_exc()
        
        print("\n🔧 Sorun giderme:")
        print("1. Tüm kütüphanelerin yüklü olduğundan emin olun:")
        print("   pip install -r requirements.txt")
        print("2. config.py dosyasının aynı klasörde olduğundan emin olun")
        print("3. Bot token ve chat ID'yi kontrol edin")
        
        try:
            messagebox.showerror("Kritik Hata", 
                               f"Program başlatılamadı:\n\n{str(e)}\n\n" +
                               "Detaylar için konsol penceresine bakın.")
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()