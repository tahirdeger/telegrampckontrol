"""
Telegram PC Controller - Sistem Kontrol Modülü
Bilgisayar durumu, ekran görüntüsü, webcam, kapatma gibi işlemleri yönetir.
"""

import platform
import psutil
import subprocess
from datetime import datetime
from PIL import ImageGrab
import config


class SystemController:
    """Sistem işlemlerini yöneten sınıf"""

    def __init__(self):
        self.os_type = platform.system()

    def get_system_status(self):
        """CPU, RAM, Disk ve sistem bilgilerini döndürür."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            uname = platform.uname()
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time

            status_message = f"""
🖥️ *Sistem Durumu*

*İşletim Sistemi:* {uname.system} {uname.release}
*Bilgisayar Adı:* {uname.node}
*İşlemci:* {uname.processor}

📊 *Performans*
• CPU: {cpu_percent}%
• RAM: {memory.percent}% ({self._format_bytes(memory.used)} / {self._format_bytes(memory.total)})
• Disk: {disk.percent}% ({self._format_bytes(disk.used)} / {self._format_bytes(disk.total)})

⏱️ *Çalışma Süresi:* {self._format_uptime(uptime)}
🕐 *Tarih/Saat:* {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
"""
            return status_message
        except Exception as e:
            return f"❌ Durum bilgisi alınamadı: {str(e)}"

    def take_screenshot(self):
        """Ekran görüntüsü alır (PNG)."""
        try:
            screenshot = ImageGrab.grab()
            import os
            shots_dir = os.path.join(os.path.dirname(__file__), "shots")
            os.makedirs(shots_dir, exist_ok=True)

            filename = datetime.now().strftime("ekran_%Y%m%d_%H%M%S.png")
            path = os.path.join(shots_dir, filename)

            screenshot.save(path, format='PNG', optimize=True, quality=config.SCREENSHOT_QUALITY)
            print(f"📸 Ekran görüntüsü kaydedildi: {path}")
            return path
        except Exception as e:
            print(f"Ekran görüntüsü hatası: {e}")
            return None

    # --------------------------------------------------------
    # 📸 WEBCAM FONKSİYONU + GİZLİLİK İZİNİ YÖNLENDİRME
    # --------------------------------------------------------
    def take_webcam_shot(self):
        """Webcam'den tek kare görüntü alır. Kamera yoksa None döner (fallback destekli)."""
        try:
            import cv2, time, os
        except Exception:
            # OpenCV yüklü değilse sessizce pas geç
            return None

        backends = [
            ("CAP_DSHOW", cv2.CAP_DSHOW),
            ("CAP_MSMF", cv2.CAP_MSMF),
            ("CAP_ANY", cv2.CAP_ANY)
        ]

        cam = None
        selected_backend = None

        try:
            for name, backend in backends:
                cam = cv2.VideoCapture(0, backend)
                if cam.isOpened():
                    selected_backend = name
                    print(f"✅ Kamera açıldı ({name})")
                    break
                else:
                    print(f"⚠️ {name} backend başarısız.")
                    cam.release()

            if cam is None or not cam.isOpened():
                print("❌ Hiçbir backend kamerayı açamadı.")
                self.prompt_camera_permission()  # Kullanıcıyı yönlendir
                return None

            # İlk birkaç kareyi at (kamera ısınsın)
            for _ in range(5):
                cam.read()
                time.sleep(0.1)

            ret, frame = cam.read()
            cam.release()

            if not ret or frame is None:
                print("⚠️ Kamera kare döndürmedi.")
                return None

            shots_dir = os.path.join(os.path.dirname(__file__), "shots")
            os.makedirs(shots_dir, exist_ok=True)

            filename = datetime.now().strftime("webcam_%Y%m%d_%H%M%S.png")
            out_path = os.path.join(shots_dir, filename)

            cv2.imwrite(out_path, frame)
            print(f"📸 Kamera görüntüsü kaydedildi: {out_path}")
            return out_path

        except Exception as e:
            print(f"Webcam hatası: {e}")
            try:
                if cam:
                    cam.release()
            except:
                pass
            return None

    # --------------------------------------------------------
    # ⚙️ SİSTEM İŞLEMLERİ
    # --------------------------------------------------------
    def shutdown_system(self):
        """Bilgisayarı kapatır."""
        if not config.SHUTDOWN_CMD:
            return False, config.ERROR_MESSAGES["unsupported_os"].format(self.os_type)
        try:
            subprocess.run(config.SHUTDOWN_CMD, shell=True, check=True)
            return True, "💤 Bilgisayar kapatılıyor... (10 saniye)"
        except subprocess.CalledProcessError as e:
            return False, config.ERROR_MESSAGES["command_failed"].format(str(e))

    def logout_session(self):
        """Kullanıcı oturumunu kapatır."""
        if not config.LOGOUT_CMD:
            return False, config.ERROR_MESSAGES["unsupported_os"].format(self.os_type)
        try:
            subprocess.run(config.LOGOUT_CMD, shell=True, check=True)
            return True, "👋 Oturum kapatılıyor..."
        except subprocess.CalledProcessError as e:
            return False, config.ERROR_MESSAGES["command_failed"].format(str(e))

    # --------------------------------------------------------
    # 🔔 GİZLİLİK İZİNLERİNE YÖNLENDİRME (KAMERA/MİKROFON/KONUM)
    # --------------------------------------------------------
    @staticmethod
    def prompt_camera_permission():
        """Kamera izni için kullanıcıya bildirim gönderir ve ayar sayfasına yönlendirir."""
        import tkinter as tk
        from tkinter import messagebox

        if platform.system() != "Windows":
            return

        root = tk.Tk()
        root.withdraw()

        msg = (
            "⚠️ Kamera erişimi engellenmiş olabilir.\n\n"
            "Bu uygulamanın kamerayı kullanabilmesi için Windows gizlilik ayarlarında "
            "'Masaüstü uygulamalarının kameraya erişmesine izin ver' seçeneğinin açık olması gerekir.\n\n"
            "Ayar sayfasını şimdi açmak ister misiniz?"
        )

        if messagebox.askyesno("Kamera Erişimi Engellendi", msg):
            try:
                subprocess.Popen(["start", "ms-settings:privacy-webcam"], shell=True)
            except Exception as e:
                messagebox.showerror("Hata", f"Ayar sayfası açılamadı:\n{e}")

    @staticmethod
    def prompt_microphone_permission():
        """Mikrofon izni için kullanıcıya bildirim gönderir."""
        import tkinter as tk
        from tkinter import messagebox

        if platform.system() != "Windows":
            return

        root = tk.Tk()
        root.withdraw()

        msg = (
            "🎙 Mikrofon erişimi engellenmiş olabilir.\n\n"
            "Bu uygulamanın mikrofonu kullanabilmesi için "
            "'Masaüstü uygulamalarının mikrofon erişimine izin ver' seçeneğini açmanız gerekir.\n\n"
            "Ayar sayfasını şimdi açmak ister misiniz?"
        )

        if messagebox.askyesno("Mikrofon Erişimi Engellendi", msg):
            try:
                subprocess.Popen(["start", "ms-settings:privacy-microphone"], shell=True)
            except Exception as e:
                messagebox.showerror("Hata", f"Ayar sayfası açılamadı:\n{e}")

    @staticmethod
    def prompt_location_permission():
        """Konum izni için kullanıcıya bildirim gönderir."""
        import tkinter as tk
        from tkinter import messagebox

        if platform.system() != "Windows":
            return

        root = tk.Tk()
        root.withdraw()

        msg = (
            "📍 Konum erişimi devre dışı olabilir.\n\n"
            "Bu uygulamanın konum bilgisine erişebilmesi için "
            "'Masaüstü uygulamalarının konum erişimine izin ver' seçeneğini açmanız gerekir.\n\n"
            "Ayar sayfasını şimdi açmak ister misiniz?"
        )

        if messagebox.askyesno("Konum Erişimi Devre Dışı", msg):
            try:
                subprocess.Popen(["start", "ms-settings:privacy-location"], shell=True)
            except Exception as e:
                messagebox.showerror("Hata", f"Ayar sayfası açılamadı:\n{e}")

    # --------------------------------------------------------
    # 🧮 YARDIMCI METODLAR
    # --------------------------------------------------------
    @staticmethod
    def _format_bytes(bytes_value):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"

    @staticmethod
    def _format_uptime(uptime):
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        parts = []
        if days > 0:
            parts.append(f"{days} gün")
        if hours > 0:
            parts.append(f"{hours} saat")
        if minutes > 0:
            parts.append(f"{minutes} dakika")
        return ", ".join(parts) if parts else "Az önce başlatıldı"


# --------------------------------------------------------
# 🔮 GELECEK ÖZELLİKLER İÇİN ŞABLON
# --------------------------------------------------------
class FutureFeatures:
    @staticmethod
    def example_volume_control(level):
        pass

    @staticmethod
    def example_open_application(app_name):
        pass
