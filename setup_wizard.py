"""
Telegram PC Controller - İlk Kurulum Sihirbazı
İlk çalıştırmada kullanıcıyı adım adım yönlendirir
"""

import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import os
import re
import json
import config


class SetupWizard:
    """İlk kurulum sihirbazı"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PC Controller - Kurulum Sihirbazı")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        # Veriler
        self.bot_token = ""
        self.chat_id = ""
        self.autostart = False
        self.autostart_bot = False
        
        # Mevcut sayfa
        self.current_page = 0
        self.pages = []
        
        # Ana konteyner
        self.main_frame = ttk.Frame(self.root)
        
        # Sayfaları oluştur
        self.create_pages()
        
        # Navigasyon çubuğu
        self.create_navigation()
        
        # Ana konteyneri yerleştir (Navigasyonun üstüne oturması için en son pack ediyoruz)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # İlk sayfayı göster
        self.show_page(0)
    
    def create_pages(self):
        """Tüm sihirbaz sayfalarını oluşturur"""
        
        # Sayfa 1: Hoşgeldiniz
        self.pages.append(self.create_welcome_page())
        
        # Sayfa 2: Bot Token
        self.pages.append(self.create_token_page())
        
        # Sayfa 3: Chat ID
        self.pages.append(self.create_chatid_page())
        
        # Sayfa 4: Başlangıç Ayarları
        self.pages.append(self.create_startup_page())
        
        # Sayfa 5: Tamamlandı
        self.pages.append(self.create_finish_page())
    
    def create_welcome_page(self):
        """Hoşgeldiniz sayfası"""
        
        frame = ttk.Frame(self.main_frame, padding="40")
        
        # Başlık
        title = ttk.Label(frame, text="🖥️ PC Controller'a Hoş Geldiniz!", 
                         font=("Arial", 18, "bold"))
        title.pack(pady=(0, 20))
        
        # Açıklama
        description = """
Bu sihirbaz, Telegram PC Controller'ı kurmanıza yardımcı olacak.

📱 Neler yapabilirsiniz?

• Bilgisayar durumunu uzaktan kontrol edin
• Ekran görüntüsü alın
• Bilgisayarı kapatın veya oturumu kapatın
• İleride daha fazla özellik ekleyin

🔒 Güvenlik

Sadece sizin belirlediğiniz Telegram hesabı
bu botu kontrol edebilecek.

⏱️ Kurulum süresi: ~3 dakika

Başlamak için "İleri" butonuna tıklayın.
        """
        
        desc_label = ttk.Label(frame, text=description, 
                              font=("Arial", 11), justify=tk.LEFT)
        desc_label.pack(pady=20)
        
        # Bilgi kutusu
        info_frame = ttk.Frame(frame, relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=20)
        
        info_text = ttk.Label(info_frame, 
                             text="💡 İpucu: Elinizde Telegram hesabınızın açık olduğundan\n    emin olun. Kurulum sırasında gerekecek.",
                             font=("Arial", 9), foreground="blue", padding=15)
        info_text.pack()
        
        return frame
    
    def create_token_page(self):
        """Bot Token sayfası"""
        
        frame = ttk.Frame(self.main_frame, padding="40")
        
        # Başlık
        title = ttk.Label(frame, text="📱 Telegram Bot Oluşturma", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Talimatlar
        instructions = """
Adım 1: Telegram Bot Oluşturun

1. Telegram'da @BotFather'ı açın
2. /newbot komutunu gönderin
3. Bot için bir isim belirleyin (örn: "PC Kontrolcüm")
4. Bot için kullanıcı adı belirleyin (örn: "mypc_controller_bot")
5. Size verilecek TOKEN'ı kopyalayın
        """
        
        inst_label = ttk.Label(frame, text=instructions, 
                              font=("Arial", 10), justify=tk.LEFT)
        inst_label.pack(anchor=tk.W, pady=(0, 20))
        
        # BotFather'ı aç butonu
        open_button = ttk.Button(frame, text="🤖 BotFather'ı Telegram'da Aç",
                                command=lambda: webbrowser.open("https://t.me/botfather"))
        open_button.pack(pady=(0, 20))
        
        # Token girişi
        token_label = ttk.Label(frame, text="Bot Token'ınızı buraya yapıştırın:", 
                               font=("Arial", 11, "bold"))
        token_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.token_entry = ttk.Entry(frame, width=60, font=("Consolas", 10))
        self.token_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Örnek göster
        example_label = ttk.Label(frame, 
                                 text="Örnek: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
                                 font=("Arial", 9), foreground="gray")
        example_label.pack(anchor=tk.W)
        
        return frame
    
    def create_chatid_page(self):
        """Chat ID sayfası"""
        
        frame = ttk.Frame(self.main_frame, padding="40")
        
        # Başlık
        title = ttk.Label(frame, text="🔑 Chat ID Öğrenme", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Talimatlar
        instructions = """
Adım 2: Chat ID'nizi Öğrenin

1. Oluşturduğunuz bot'a Telegram'dan bir mesaj gönderin
   (örn: "merhaba" yazın)

2. Aşağıdaki butona tıklayarak web sayfasını açın

3. Açılan sayfada "chat":{"id": kısmını bulun

4. id'nin yanındaki sayıyı kopyalayın (örn: 123456789)
        """
        
        inst_label = ttk.Label(frame, text=instructions, 
                              font=("Arial", 10), justify=tk.LEFT)
        inst_label.pack(anchor=tk.W, pady=(0, 20))
        
        # URL açma butonu
        self.url_button = ttk.Button(frame, text="🌐 Chat ID Öğrenme Sayfasını Aç",
                                     command=self.open_chat_id_url,
                                     state=tk.DISABLED)
        self.url_button.pack(pady=(0, 20))
        
        # Chat ID girişi
        chatid_label = ttk.Label(frame, text="Chat ID'nizi buraya girin:", 
                                font=("Arial", 11, "bold"))
        chatid_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.chatid_entry = ttk.Entry(frame, width=60, font=("Consolas", 10))
        self.chatid_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Örnek göster
        example_label = ttk.Label(frame, 
                                 text="Örnek: 123456789 (sadece sayılar)",
                                 font=("Arial", 9), foreground="gray")
        example_label.pack(anchor=tk.W)
        
        # Uyarı
        warning_frame = ttk.Frame(frame, relief=tk.SOLID, borderwidth=1)
        warning_frame.pack(fill=tk.X, pady=(20, 0))
        
        warning_text = ttk.Label(warning_frame,
                                text="⚠️ Önemli: Önce bot'unuza mutlaka bir mesaj gönderin!\n   Yoksa Chat ID görünmeyecektir.",
                                font=("Arial", 9), foreground="orange", padding=15)
        warning_text.pack()
        
        return frame
    
    def create_startup_page(self):
        """Başlangıç ayarları sayfası"""
        
        frame = ttk.Frame(self.main_frame, padding="40")
        
        # Başlık
        title = ttk.Label(frame, text="⚙️ Başlangıç Ayarları", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Açıklama
        description = ttk.Label(frame,
                               text="Son adım! Programın nasıl başlamasını istersiniz?",
                               font=("Arial", 11))
        description.pack(pady=(0, 30))
        
        # Seçenek 1: Windows başlangıcı
        startup_frame = ttk.LabelFrame(frame, text="Windows Başlangıcı", padding=20)
        startup_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.autostart_var = tk.BooleanVar(value=True)
        autostart_check = ttk.Checkbutton(startup_frame,
                                         text="Windows açılışında programı otomatik başlat",
                                         variable=self.autostart_var)
        autostart_check.pack(anchor=tk.W)
        
        autostart_desc = ttk.Label(startup_frame,
                                  text="Program Windows başladığında otomatik olarak\narka planda çalışmaya başlar.",
                                  font=("Arial", 9), foreground="gray")
        autostart_desc.pack(anchor=tk.W, pady=(5, 0))
        
        # Seçenek 2: Bot otomatik başlat
        bot_frame = ttk.LabelFrame(frame, text="Bot Başlatma", padding=20)
        bot_frame.pack(fill=tk.X)
        
        self.autostart_bot_var = tk.BooleanVar(value=True)
        autostart_bot_check = ttk.Checkbutton(bot_frame,
                                             text="Program açıldığında bot'u otomatik başlat",
                                             variable=self.autostart_bot_var)
        autostart_bot_check.pack(anchor=tk.W)
        
        bot_desc = ttk.Label(bot_frame,
                            text="Program her açıldığında bot servisi otomatik olarak\nbaşlar ve sistem tepsisine küçülür.",
                            font=("Arial", 9), foreground="gray")
        bot_desc.pack(anchor=tk.W, pady=(5, 0))
        
        # Öneri
        recommend_frame = ttk.Frame(frame, relief=tk.SOLID, borderwidth=1)
        recommend_frame.pack(fill=tk.X, pady=(20, 0))
        
        recommend_text = ttk.Label(recommend_frame,
                                  text="💡 Önerilen: Her iki seçeneği de işaretleyin.\n   Böylece bilgisayarınız her açıldığında bot aktif olur.",
                                  font=("Arial", 9), foreground="blue", padding=15)
        recommend_text.pack()
        
        return frame
    
    def create_finish_page(self):
        """Tamamlanma sayfası"""
        
        frame = ttk.Frame(self.main_frame, padding="40")
        
        # Başlık
        title = ttk.Label(frame, text="✅ Kurulum Tamamlandı!", 
                         font=("Arial", 18, "bold"), foreground="green")
        title.pack(pady=(0, 20))
        
        # Başarı mesajı
        success_msg = """
Tebrikler! PC Controller başarıyla kuruldu.

📱 Botunuza şu komutları gönderebilirsiniz:

/start      → Hoşgeldin mesajı
/status     → Sistem durumu
/screenshot → Ekran görüntüsü
/logout     → Oturumu kapat
/shutdown   → Bilgisayarı kapat

🎯 Şimdi ne yapmalısınız?

1. "Bitir" butonuna tıklayın
2. Program açılacak ve bot başlayacak
3. Telegram'dan bot'unuza komut gönderin
4. Keyfini çıkarın! 🎉
        """
        
        success_label = ttk.Label(frame, text=success_msg,
                                 font=("Arial", 11), justify=tk.LEFT)
        success_label.pack(pady=20)
        
        # Bilgi kutusu
        info_frame = ttk.Frame(frame, relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=20)
        
        info_text = ttk.Label(info_frame,
                             text="💡 İpucu: Program sistem tepsisine küçülecek.\n   Görmek için sağ alt köşedeki ^ simgesine tıklayın.",
                             font=("Arial", 9), foreground="blue", padding=15)
        info_text.pack()
        
        return frame
    
    def create_navigation(self):
        """Navigasyon çubuğunu oluşturur"""
        
        nav_frame = ttk.Frame(self.root, padding="10")
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Geri butonu
        self.back_button = ttk.Button(nav_frame, text="← Geri",
                                      command=self.previous_page)
        self.back_button.pack(side=tk.LEFT)
        
        # İlerleme göstergesi
        self.progress_label = ttk.Label(nav_frame, text="1 / 5",
                                       font=("Arial", 10))
        self.progress_label.pack(side=tk.LEFT, padx=20)
        
        # İleri/Bitir butonu
        self.next_button = ttk.Button(nav_frame, text="İleri →",
                                      command=self.next_page)
        self.next_button.pack(side=tk.RIGHT)
        
        # İptal butonu
        self.cancel_button = ttk.Button(nav_frame, text="İptal",
                                        command=self.cancel_setup)
        self.cancel_button.pack(side=tk.RIGHT, padx=(0, 10))
    
    def show_page(self, page_num):
        """Belirtilen sayfayı gösterir"""
        
        # Tüm sayfaları gizle
        for page in self.pages:
            page.pack_forget()
        
        # İstenen sayfayı göster
        self.pages[page_num].pack(fill=tk.BOTH, expand=True)
        self.current_page = page_num
        
        # Buton durumlarını güncelle
        self.update_navigation()
    
    def update_navigation(self):
        """Navigasyon butonlarını günceller"""
        
        # Geri butonu
        if self.current_page == 0:
            self.back_button.configure(state=tk.DISABLED)
        else:
            self.back_button.configure(state=tk.NORMAL)
        
        # İleri/Bitir butonu
        if self.current_page == len(self.pages) - 1:
            self.next_button.configure(text="Bitir ✓")
            self.cancel_button.configure(state=tk.DISABLED)
        else:
            self.next_button.configure(text="İleri →")
            self.cancel_button.configure(state=tk.NORMAL)
        
        # İlerleme
        self.progress_label.configure(text=f"{self.current_page + 1} / {len(self.pages)}")
    
    def previous_page(self):
        """Önceki sayfaya gider"""
        
        if self.current_page > 0:
            self.show_page(self.current_page - 1)
    
    def next_page(self):
        """Sonraki sayfaya gider veya kurulumu tamamlar"""
        
        # Son sayfada mı?
        if self.current_page == len(self.pages) - 1:
            self.finish_setup()
            return
        
        # Sayfa validasyonu
        if not self.validate_current_page():
            return
        
        # Sonraki sayfaya geç
        self.show_page(self.current_page + 1)
    
    def validate_current_page(self):
        """Mevcut sayfanın verilerini doğrular"""
        
        # Token sayfası
        if self.current_page == 1:
            token = self.token_entry.get().strip()
            if not token:
                messagebox.showerror("Hata", "Lütfen Bot Token'ınızı girin!")
                return False
            if len(token) < 20:
                messagebox.showerror("Hata", "Geçersiz token formatı!\n\nToken'ınızı BotFather'dan doğru kopyaladığınızdan emin olun.")
                return False
            self.bot_token = token
            # URL butonunu aktifleştir
            self.url_button.configure(state=tk.NORMAL)
        
        # Chat ID sayfası
        elif self.current_page == 2:
            chat_id = self.chatid_entry.get().strip()
            if not chat_id:
                messagebox.showerror("Hata", "Lütfen Chat ID'nizi girin!")
                return False
            try:
                int(chat_id)
            except ValueError:
                messagebox.showerror("Hata", "Chat ID sadece sayılardan oluşmalıdır!")
                return False
            self.chat_id = chat_id
        
        # Başlangıç ayarları sayfası
        elif self.current_page == 3:
            self.autostart = self.autostart_var.get()
            self.autostart_bot = self.autostart_bot_var.get()
        
        return True
    
    def open_chat_id_url(self):
        """Chat ID öğrenme URL'sini açar"""
        
        url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
        webbrowser.open(url)
    
    def cancel_setup(self):
        """Kurulumu iptal eder"""
        
        if messagebox.askyesno("İptal", "Kurulumdan çıkmak istediğinize emin misiniz?"):
            self.root.quit()
            self.root.destroy()
            self.setup_completed = False
    
    def finish_setup(self):
        """Kurulumu tamamlar ve ayarları kaydeder"""
        
        try:
            # config.py dosyasını güncelle
            self.save_config()
            
            # Windows başlangıcına ekle (gerekirse)
            if self.autostart:
                self.add_to_startup()
            
            messagebox.showinfo("Başarılı", 
                              "Kurulum tamamlandı!\n\n" +
                              "Program şimdi başlayacak.")
            
            self.setup_completed = True
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Hata", 
                               f"Kurulum tamamlanamadı:\n\n{str(e)}\n\n" +
                               "Ayarları manuel olarak config.py'den değiştirmeyi deneyin.")
            self.setup_completed = False
    
    def save_config(self):
        """Ayarları secret.json dosyasına kaydeder"""
        
        secret_path = os.path.join(config.get_base_path(), "secret.json")
        
        # Mevcut veriyi oku veya yeni oluştur
        data = {}
        if os.path.exists(secret_path):
            try:
                with open(secret_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except:
                pass
        
        # Verileri güncelle
        data["BOT_TOKEN"] = self.bot_token
        data["AUTHORIZED_CHAT_ID"] = int(self.chat_id)
        data["AUTOSTART_BOT"] = self.autostart_bot
        
        # Kaydet
        with open(secret_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    
    def add_to_startup(self):
        """Windows başlangıcına ekler"""
        
        import platform
        if platform.system() != "Windows":
            return
        
        try:
            import winreg
            import sys
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run")
            
            if getattr(sys, 'frozen', False):
                # .exe olarak çalışıyorsa
                exe_path = os.path.abspath(sys.executable)
                command = f'"{exe_path}"'
            else:
                # .py olarak çalışıyorsa, python.exe ile betiği çalıştırmalı
                # pythonw.exe kullanırsak konsol penceresi açılmaz (tercihen)
                python_exe = sys.executable.replace("python.exe", "pythonw.exe")
                if not os.path.exists(python_exe): 
                    python_exe = sys.executable # pythonw yoksa normal python kullan
                
                script_path = os.path.abspath(sys.argv[0])
                command = f'"{python_exe}" "{script_path}"'
            
            # Önce eski kaydı temizle
            try:
                winreg.DeleteValue(key, "PCControllerBot")
            except FileNotFoundError:
                pass
            
            winreg.SetValueEx(key, "PCControllerBot", 0, winreg.REG_SZ, command)
            winreg.CloseKey(key)
            # Kullanıcıya bilgi verelim (Log veya print)
            print(f"✅ Windows başlangıcına eklendi: {command}")
            
        except Exception as e:
            print(f"❌ Başlangıca ekleme hatası: {e}")
            # Hata olsa bile programın kapanmaması için sessizce devam edebilir veya uyarabiliriz
            # messagebox.showerror("Hata", f"Başlangıç ayarı yapılamadı: {e}")
    
    def run(self):
        """Sihirbazı çalıştırır"""
        
        self.setup_completed = False
        self.root.mainloop()
        return self.setup_completed


def check_if_first_run():
    """İlk çalıştırma kontrolü yapar"""
    
    import config
    
    # Token veya Chat ID ayarlanmamışsa ilk çalıştırmadır
    if (not config.BOT_TOKEN or 
        config.BOT_TOKEN == "BURAYA_BOT_TOKEN_YAZIN" or
        config.AUTHORIZED_CHAT_ID == 0):
        return True
    
    return False


if __name__ == "__main__":
    wizard = SetupWizard()
    wizard.run()