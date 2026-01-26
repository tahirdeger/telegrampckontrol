"""
Telegram PC Controller - Grafik Arayüz Modülü
Modern GUI, sistem tepsisi, sohbet ve bildirim
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import queue
import sys
import os
from datetime import datetime
import pystray
from PIL import Image, ImageDraw
import config
import webbrowser


class PCControllerGUI:
    """Ana GUI penceresi"""

    def __init__(self, bot_handler):
        self.bot_handler = bot_handler
        self.root = tk.Tk()

        # 🔹 Modern Tema Ayarları
        style = ttk.Style()
        style.theme_use("clam")

        # Ana renk paleti
        bg_main = "#f4f6f8"
        bg_frame = "#ffffff"
        accent = "#2f6feb"  # vurgulu mavi
        text_color = "#222"
        gray_text = "#555"

        # Arka planlar
        self.root.configure(bg=bg_main)
        style.configure("TFrame", background=bg_frame)
        style.configure("TLabelFrame", background=bg_frame, foreground=text_color)
        style.configure("TLabel", background=bg_frame, foreground=text_color)

        # Butonlar
        style.configure("TButton",
                        background=accent,
                        foreground="white",
                        font=("Segoe UI", 9, "bold"),
                        borderwidth=0)
        style.map("TButton",
                  background=[("active", "#1e4ed8")],
                  foreground=[("active", "white")])

        # Sekmeler (Notebook)
        style.configure("TNotebook", background=bg_main, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background="#e5e7eb",
                        foreground="#333",
                        padding=(12, 6),
                        font=("Segoe UI", 9, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", accent)],
                  foreground=[("selected", "white")])

        self.root.title("PC Controller - Telegram Bot")
        self.root.geometry("700x560")
        self.root.minsize(620, 520)

        # Pencere kapatma → tepsiye
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

        # Log mesajları için kuyruk
        self.log_queue = queue.Queue()

        # Sistem tepsisi ikonu
        self.tray_icon = None

        # Bot thread ve durum
        self.bot_thread = None
        self.bot_running = False
        self.bot_application = None  # Telegram Application

        # GUI oluştur
        self.create_gui()

        # GUI → Bot: sohbet callback & aktivite log
        try:
            def gui_callback_with_log(sender, text):
                self.add_chat_message(sender, text)
                self.add_log(f"{sender}: {text}", "TELEGRAM")

            self.bot_handler.set_gui_callback(gui_callback_with_log)
        except Exception:
            pass

        # Log güncelleyici
        self.update_log_display()

    # ---------------- GUI Kurulum ----------------
    def create_gui(self):
        """GUI bileşenlerini oluşturur"""
         # Tema ayarları (aktif sekme gri, pasif sekme mavi ve ince)
        style = ttk.Style()
        style.theme_use("clam")

        # Çerçeveler ve butonlar
        style.configure("TLabelFrame", background="#f5f7fa")
        style.configure("TFrame", background="#f7f9fb")

        style.configure("TButton",
                        background="#4a90e2",
                        foreground="white",
                        font=("Segoe UI", 9, "bold"),
                        relief="flat")
        style.map("TButton",
                  background=[("active", "#357ABD")],
                  relief=[("pressed", "sunken")])

        # Notebook sekmeleri
        style.configure("TNotebook", background="#dfe6f1", borderwidth=0)
        style.configure("TNotebook.Tab",
                        font=("Segoe UI", 9, "bold"),
                        padding=[10, 4],
                        background="#4a90e2",
                        foreground="white",
                        relief="flat")

        # Seçili sekme: gri ve geniş, diğerleri mavi ve dar
        style.map("TNotebook.Tab",
                  background=[("selected", "#f2f2f2"), ("!selected", "#4a90e2")],
                  foreground=[("selected", "#000000"), ("!selected", "#ffffff")],
                  padding=[("selected", [14, 8])])  # aktif sekme yüksek görünür
        
        # Grid altyapısı
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Üst: Durum
        status_frame = ttk.LabelFrame(main_frame, text="Bot Durumu", padding="10")
        status_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)

        ttk.Label(status_frame, text="Durum:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.status_label = ttk.Label(status_frame, text="⚪ Durduruldu",
                                    foreground="gray", font=("Arial", 10, "bold"))
        self.status_label.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(status_frame, text="Yetkili Chat ID:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        chat_id_text = str(config.AUTHORIZED_CHAT_ID) if config.AUTHORIZED_CHAT_ID != 0 else "Ayarlanmamış"
        self.chat_id_label = ttk.Label(status_frame, text=chat_id_text)
        self.chat_id_label.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))

        ttk.Label(status_frame, text="İşletim Sistemi:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.os_label = ttk.Label(status_frame, text=config.OS_TYPE)
        self.os_label.grid(row=2, column=1, sticky=tk.W, pady=(5, 0))

        # Orta: Kontrol butonları
        control_frame = ttk.LabelFrame(main_frame, text="Kontrol", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)

        self.start_button = ttk.Button(button_frame, text="▶ Botu Başlat",
                                    command=self.toggle_bot, width=20)
        self.start_button.pack(side=tk.LEFT, padx=(0, 5))

        self.settings_button = ttk.Button(button_frame, text="⚙ Ayarlar",
                                        command=self.open_settings, width=15)
        self.settings_button.pack(side=tk.LEFT, padx=(0, 5))

        self.minimize_button = ttk.Button(button_frame, text="🗕 Tepsiye Küçült",
                                        command=self.minimize_to_tray, width=18)
        self.minimize_button.pack(side=tk.LEFT, padx=(0, 5))

        self.exit_button = ttk.Button(button_frame, text="❌ Uygulamayı Kapat",
                                    command=self.quit_application, width=20)
        self.exit_button.pack(side=tk.LEFT, padx=(0, 5))

        # Notebook (Sohbet + Log) - Sıralama tersine çevrildi
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=3, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        main_frame.rowconfigure(3, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # 1️⃣ Sohbet sekmesi (öncelikli ve geniş)
        chat_frame = ttk.Frame(notebook, padding="10")
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        notebook.add(chat_frame, text="💬 Sohbet (Telegram ↔ PC)")

        self.chat_box = scrolledtext.ScrolledText(chat_frame, height=18,
                                                wrap=tk.WORD, state=tk.DISABLED,
                                                font=("Consolas", 10))
        self.chat_box.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        chat_entry_frame = ttk.Frame(chat_frame)
        chat_entry_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(8, 0))
        chat_entry_frame.columnconfigure(0, weight=1)

        self.chat_entry = ttk.Entry(chat_entry_frame)
        self.chat_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.chat_entry.bind("<Return>", lambda e: self.send_chat_message())

        send_btn = ttk.Button(chat_entry_frame, text="Gönder",
                            command=self.send_chat_message, width=12)
        send_btn.grid(row=0, column=1, padx=(8, 0))

        # 2️⃣ Aktivite Günlüğü sekmesi (daha sade ve kısa)
        log_frame = ttk.Frame(notebook, padding="10")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        notebook.add(log_frame, text="📜 Aktivite Günlüğü")

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10,
                                                wrap=tk.WORD, state=tk.DISABLED,
                                                font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        clear_button = ttk.Button(log_frame, text="🗑 Günlüğü Temizle",
                                command=self.clear_log)
        clear_button.grid(row=1, column=0, pady=(5, 0), sticky=tk.W)

        # Footer (tıklanabilir bağlantı)
        footer = ttk.Label(
            self.root,
            text="Üretici: TAHIR  |  Bilgi için: islematolyesi.odoo.com",
            font=("Arial", 9, "italic"),
            foreground="#0078d7",
            cursor="hand2"
        )
        footer.grid(row=1, column=0, sticky=(tk.E, tk.W), pady=(0, 6))
        footer.bind("<Button-1>", lambda e: webbrowser.open("https://islematolyesi.odoo.com"))

        # Varsayılan sekme sohbet
        notebook.select(0)

        # İlk log
        self.add_log("Program başlatıldı", "INFO")


    # ---------------- Bot Başlat/Durdur ----------------
    def toggle_bot(self):
        """Bot'u başlatır veya durdurur"""
        if not self.bot_running:
            if not config.BOT_TOKEN or config.BOT_TOKEN == "BURAYA_BOT_TOKEN_YAZIN":
                messagebox.showerror("Yapılandırma Hatası", 
                    "Bot token ayarlanmamış!\n\nAyarlar butonuna tıklayarak token'ınızı girin.")
                return
            if config.AUTHORIZED_CHAT_ID == 0:
                messagebox.showerror("Yapılandırma Hatası",
                    "Chat ID ayarlanmamış!\n\nAyarlar butonuna tıklayarak chat ID'nizi girin.")
                return
            self.start_bot()
        else:
            self.stop_bot()
    
    def start_bot(self):
        """Botu arka planda başlatır"""
        if self.bot_running:
            self.add_log("Bot zaten çalışıyor!", "WARNING")
            messagebox.showwarning("Uyarı", "Bot zaten çalışıyor!")
            return
        
        self.bot_running = True
        self.start_button.configure(text="⏹ Botu Durdur")
        self.status_label.configure(text="🟢 Çalışıyor", foreground="green")
        self.settings_button.configure(state=tk.DISABLED)
        
        self.add_log("Bot başlatılıyor...", "INFO")
        
        self.bot_thread = threading.Thread(target=self._run_bot, daemon=True)
        self.bot_thread.start()
    
    def _run_bot(self):
        """Bot'u çalıştıran thread fonksiyonu"""
        try:
            import asyncio
            self.add_log(f"Bot aktif - Chat ID: {config.AUTHORIZED_CHAT_ID}", "SUCCESS")
            self.add_log(f"İşletim Sistemi: {config.OS_TYPE}", "INFO")
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Botu çalıştır
            self.bot_application = self.bot_handler.run()
        except Exception as e:
            self.add_log(f"Bot hatası: {str(e)}", "ERROR")
            self.bot_running = False
            self.root.after(0, self._reset_ui_after_error)
    
    def _reset_ui_after_error(self):
        self.start_button.configure(text="▶ Botu Başlat")
        self.status_label.configure(text="🔴 Hata", foreground="red")
        self.settings_button.configure(state=tk.NORMAL)
    
    # ✅ Güncellenmiş: Durdurunca AUTOSTART_BOT kapat + restart
    def stop_bot(self):
        """Botu durdurur ve otomatik başlatmayı devre dışı bırakır"""
        if not self.bot_running:
            return

        self.add_log("⚠️ Bot durduruluyor... (Program yeniden başlatılacak)", "WARNING")

        # AUTOSTART_BOT → False
        try:
            with open('config.py', 'r', encoding='utf-8') as f:
                content = f.read()
            import re
            if 'AUTOSTART_BOT' in content:
                content = re.sub(r'AUTOSTART_BOT\s*=\s*True', 'AUTOSTART_BOT = False', content)
            else:
                content += "\n\n# Otomatik başlatma\nAUTOSTART_BOT = False\n"
            with open('config.py', 'w', encoding='utf-8') as f:
                f.write(content)
            self.add_log("AUTOSTART_BOT devre dışı bırakıldı", "INFO")
        except Exception as e:
            self.add_log(f"Config güncellenemedi: {e}", "ERROR")
            messagebox.showwarning("Uyarı", f"Ayar dosyası güncellenemedi:\n{e}")

        self.bot_running = False
        self.status_label.configure(text="⚪ Durduruldu", foreground="gray")
        self.start_button.configure(text="▶ Botu Başlat", state=tk.DISABLED)
        self.settings_button.configure(state=tk.DISABLED)

        messagebox.showinfo(
            "Bilgi",
            "🤖 Bot durduruldu ve otomatik başlatma devre dışı bırakıldı.\n"
            "Program şimdi yeniden başlatılacak."
        )

        self.restart_application()
    
    # ---------------- Restart / Exit ----------------
    def restart_application(self):
        self.add_log("Program yeniden başlatılıyor...", "INFO")
        if self.bot_running:
            self.bot_running = False
        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except:
                pass
        python = sys.executable
        script = os.path.abspath(sys.argv[0])
        self.root.after(500, lambda: self._do_restart(python, script))
    
    def _do_restart(self, python, script):
        try:
            self.root.destroy()
            os.execl(python, python, script)
        except Exception as e:
            print(f"Yeniden başlatma hatası: {e}")
            sys.exit(0)
    
    def quit_application(self, icon=None, item=None):
        """Uygulamayı tamamen kapatır"""
        # Tepsi ikonu varsa kapat
        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except:
                pass
        # Pencereyi kapat
        self.root.after(0, self.root.quit)
    
    # ---------------- Ayarlar / Log ----------------
    def open_settings(self):
        SettingsWindow(self.root, self)
    
    def add_log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        self.log_queue.put((log_entry, level))
    
    def update_log_display(self):
        try:
            while True:
                log_entry, level = self.log_queue.get_nowait()
                self.log_text.configure(state=tk.NORMAL)
                self.log_text.insert(tk.END, log_entry)
                self.log_text.see(tk.END)
                self.log_text.configure(state=tk.DISABLED)
        except queue.Empty:
            pass
        self.root.after(100, self.update_log_display)
    
    def clear_log(self):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state=tk.DISABLED)
        self.add_log("Günlük temizlendi", "INFO")
    
    # ---------------- Sistem Tepsisi ----------------
    def minimize_to_tray(self):
        """Pencereyi sistem tepsisine küçültür"""
        self.root.withdraw()
        if self.tray_icon is None:
            self.create_tray_icon()
        self.add_log("Sistem tepsisine küçültüldü", "INFO")
    
    def create_tray_icon(self):
        image = Image.new('RGB', (64, 64), color=(0, 120, 215))
        dc = ImageDraw.Draw(image)
        dc.rectangle([16, 16, 48, 48], fill=(255, 255, 255))
        
        menu = pystray.Menu(
            pystray.MenuItem("Göster", self.show_window),
            pystray.MenuItem("Başlat/Durdur", self.toggle_bot_from_tray),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Çıkış", self.quit_application)
        )
        
        self.tray_icon = pystray.Icon("PC Controller", image, "PC Controller Bot", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()
    
    def show_window(self, icon=None, item=None):
        self.root.after(0, self._show_window)
    
    def _show_window(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def toggle_bot_from_tray(self, icon=None, item=None):
        self.root.after(0, self.toggle_bot)
    
    # ---------------- Sohbet ----------------
    def add_chat_message(self, sender, text):
        """Telegram’dan gelen veya GUI’den gönderilen mesajı sohbet paneline yazar.
           Pencere gizliyse bildirim gösterir."""
        self.chat_box.configure(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"{sender}: {text}\n")
        self.chat_box.configure(state=tk.DISABLED)
        self.chat_box.see(tk.END)
        
        # Pencere gizli ise bildirim
        if not self.root.winfo_viewable():
            self._notify("Yeni Telegram Mesajı", text)
    
    def send_chat_message(self):
        msg = self.chat_entry.get().strip()
        if not msg:
            return
        sent = self.bot_handler.send_text_to_authorized_chat(msg)
        if sent:
            self.add_chat_message("Siz", msg)
            self.chat_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Uyarı", "Mesaj gönderilemedi. Bot çalışıyor mu?")

    
    def _notify(self, title, message):
        """Tepsi bildirimi (opsiyonel plyer). Plyer yoksa sessiz geç."""
        try:
            from plyer import notification
            notification.notify(title=title, message=message, app_name="PC Controller", timeout=5)
        except Exception:
            # Plyer yoksa problemsiz atla
            pass
    
    # ---------------- Mainloop ----------------
    def run(self):
        self.root.mainloop()


# ============================================
# AYARLAR PENCERESİ
# ============================================

class SettingsWindow:
    """Ayarlar penceresi"""
    
    def __init__(self, parent, main_gui):
        self.main_gui = main_gui
        self.window = tk.Toplevel(parent)
        self.window.title("Ayarlar")
        self.window.geometry("550x500")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_settings_gui()
    
    def create_settings_gui(self):
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # BOT AYARLARI
        bot_frame = ttk.Frame(notebook, padding="20")
        notebook.add(bot_frame, text="Bot Ayarları")
        
        ttk.Label(bot_frame, text="Bot Token:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.token_entry = ttk.Entry(bot_frame, width=50, show="*")
        self.token_entry.insert(0, config.BOT_TOKEN)
        self.token_entry.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(bot_frame, text="Token'ı görmek için aşağıdaki butona tıklayın", 
                 foreground="gray", font=("Arial", 8)).pack(anchor=tk.W)
        
        show_token_btn = ttk.Button(bot_frame, text="👁 Token'ı Göster/Gizle", 
                                    command=lambda: self.toggle_password(self.token_entry))
        show_token_btn.pack(anchor=tk.W, pady=(0, 15))
        
        ttk.Label(bot_frame, text="Yetkili Chat ID:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.chat_id_entry = ttk.Entry(bot_frame, width=50)
        self.chat_id_entry.insert(0, str(config.AUTHORIZED_CHAT_ID))
        self.chat_id_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(bot_frame, text="Chat ID'nizi öğrenmek için:", 
                 foreground="gray", font=("Arial", 8)).pack(anchor=tk.W)
        ttk.Label(bot_frame, text="1. Botunuza mesaj gönderin", 
                 foreground="gray", font=("Arial", 8)).pack(anchor=tk.W)
        ttk.Label(bot_frame, text="2. https://api.telegram.org/bot<TOKEN>/getUpdates", 
                 foreground="gray", font=("Arial", 8)).pack(anchor=tk.W)
        ttk.Label(bot_frame, text="   adresini ziyaret edin", 
                 foreground="gray", font=("Arial", 8)).pack(anchor=tk.W, pady=(0, 15))
        
        info_frame = ttk.Frame(bot_frame, relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        info_text = ttk.Label(info_frame,
                             text="💡 İpucu: Bot token veya Chat ID değiştiğinde\n   program otomatik olarak yeniden başlar.",
                             font=("Arial", 9), foreground="blue", padding=10)
        info_text.pack()
        
        save_btn = ttk.Button(bot_frame, text="💾 Kaydet ve Yeniden Başlat", command=self.save_bot_settings)
        save_btn.pack(pady=(10, 0))
        
        # BAŞLANGIÇ AYARLARI
        startup_frame = ttk.Frame(notebook, padding="20")
        notebook.add(startup_frame, text="Başlangıç")
        
        ttk.Label(startup_frame, text="Otomatik Başlatma", 
                 font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 20))
        
        self.startup_var = tk.BooleanVar(value=self.check_startup_status())
        startup_check = ttk.Checkbutton(startup_frame, 
                                       text="Windows başlangıcında otomatik başlat",
                                       variable=self.startup_var,
                                       command=self.toggle_startup)
        startup_check.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(startup_frame, text="Bu seçenek etkinleştirildiğinde, program\nWindows açılışında otomatik olarak başlar ve\nsistem tepsisine küçülmüş halde bekler.", 
                 foreground="gray", font=("Arial", 9)).pack(anchor=tk.W, pady=(10, 20))
        
        self.autostart_bot_var = tk.BooleanVar(value=getattr(config, 'AUTOSTART_BOT', False))
        autostart_check = ttk.Checkbutton(startup_frame,
                                         text="Program açılınca bot'u otomatik başlat",
                                         variable=self.autostart_bot_var)
        autostart_check.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(startup_frame, text="Program başladığında bot servisi otomatik olarak\nbaşlatılır ve sistem tepsisine küçülür.", 
                 foreground="gray", font=("Arial", 9)).pack(anchor=tk.W, pady=(10, 20))
        
        info_frame2 = ttk.Frame(startup_frame, relief=tk.SOLID, borderwidth=1)
        info_frame2.pack(fill=tk.X, pady=(0, 20))
        info_text2 = ttk.Label(info_frame2,
                             text="💡 İpucu: Ayarları kaydettikten sonra program\n   otomatik olarak yeniden başlatılacak.",
                             font=("Arial", 9), foreground="blue", padding=15)
        info_text2.pack()
        
        save_startup_btn = ttk.Button(startup_frame, text="💾 Kaydet ve Yeniden Başlat", 
                                     command=self.save_startup_settings)
        save_startup_btn.pack(pady=(10, 0))
    
    def toggle_password(self, entry):
        entry.configure(show='' if entry.cget('show') == '*' else '*')
    
    def save_bot_settings(self):
        """Bot token ve chat ID'yi secret.json dosyasına kaydeder."""
        import json
        secret_path = os.path.join(config.get_base_path(), "secret.json")

        new_token = self.token_entry.get().strip()
        new_chat_id = self.chat_id_entry.get().strip()

        if not new_token or new_token == "BURAYA_BOT_TOKEN_YAZIN":
            messagebox.showerror("Hata", "Geçerli bir bot token girin!")
            return

        try:
            chat_id = int(new_chat_id)
        except ValueError:
            messagebox.showerror("Hata", "Chat ID sayı olmalıdır!")
            return

        try:
            # secret.json varsa oku, yoksa yeni oluştur
            if os.path.exists(secret_path):
                with open(secret_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {}

            data["BOT_TOKEN"] = new_token
            data["AUTHORIZED_CHAT_ID"] = chat_id

            # JSON'u yaz
            with open(secret_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            # GUI güncelle
            self.main_gui.chat_id_label.configure(text=str(chat_id))

            result = messagebox.askyesno(
                "Başarılı",
                "✅ Bot ayarları secret.json dosyasına kaydedildi!\n\n"
                "Ayarların geçerli olması için programın\n"
                "yeniden başlatılması gerekiyor.\n\n"
                "Şimdi yeniden başlatmak ister misiniz?"
            )
            if result:
                self.window.destroy()
                self.main_gui.restart_application()
            else:
                self.window.destroy()

        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar kaydedilemedi:\n{str(e)}")

    
    def check_startup_status(self):
        import platform
        if platform.system() != "Windows":
            return False
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, "PCControllerBot")
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except:
            return False
    
    def toggle_startup(self):
        import platform
        if platform.system() != "Windows":
            messagebox.showwarning("Uyarı", "Bu özellik sadece Windows'ta çalışır!")
            self.startup_var.set(False)
            return
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_SET_VALUE)
            if self.startup_var.get():
                exe_path = os.path.abspath(sys.argv[0])
                winreg.SetValueEx(key, "PCControllerBot", 0, winreg.REG_SZ, f'"{exe_path}"')
                messagebox.showinfo("Başarılı", "Otomatik başlatma etkinleştirildi!")
            else:
                try:
                    winreg.DeleteValue(key, "PCControllerBot")
                    messagebox.showinfo("Başarılı", "Otomatik başlatma devre dışı bırakıldı!")
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            messagebox.showerror("Hata", f"İşlem başarısız:\n{str(e)}")
            self.startup_var.set(self.check_startup_status())
    
    def save_startup_settings(self):
        try:
            with open('config.py', 'r', encoding='utf-8') as f:
                content = f.read()
            import re
            if 'AUTOSTART_BOT' in content:
                content = re.sub(
                    r'AUTOSTART_BOT = (True|False)',
                    f'AUTOSTART_BOT = {self.autostart_bot_var.get()}',
                    content
                )
            else:
                content += f"\n\n# Otomatik başlatma\nAUTOSTART_BOT = {self.autostart_bot_var.get()}\n"
            with open('config.py', 'w', encoding='utf-8') as f:
                f.write(content)
            import importlib
            importlib.reload(config)
            result = messagebox.askyesno(
                "Başarılı",
                "✅ Başlangıç ayarları kaydedildi!\n\n"
                "Ayarların geçerli olması için programı\n"
                "yeniden başlatmak gerekiyor.\n\n"
                "Şimdi yeniden başlatmak ister misiniz?"
            )
            if result:
                self.window.destroy()
                self.main_gui.restart_application()
            else:
                self.window.destroy()
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar kaydedilemedi:\n{str(e)}")
