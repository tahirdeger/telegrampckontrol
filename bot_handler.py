"""
Telegram PC Controller - Bot Yönetici Modülü
Telegram mesajlarını alır ve sistem komutlarına yönlendirir.
"""

import logging
import threading
import asyncio
import platform
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import config
from system_control import SystemController


class BotHandler:
    """Telegram bot işlemlerini yöneten sınıf"""
    
    def __init__(self):
        self.system = SystemController()
        self.application = None  # Application nesnesi
        self.bot_loop = None     # Çalışan asyncio döngüsü
        self.gui_callback = None # GUI'ye mesaj iletmek için callback
        
        if config.ENABLE_LOGGING:
            logging.basicConfig(
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level=logging.INFO
            )
            self.logger = logging.getLogger(__name__)

    # ---------- GUI ile entegrasyon ----------
    def set_gui_callback(self, callback_fn):
        """GUI tarafında sohbet penceresini güncellemek için callback kaydı."""
        self.gui_callback = callback_fn

    def send_text_to_authorized_chat(self, text: str) -> bool:
        """
        GUI'den Telegram'a mesaj gönderir.
        - Bot kapalıysa False döner.
        - Bot açıksa mevcut event loop'a thread-safe gönderim yapar.
        """
        try:
            app = self.application
            if not app or not getattr(app, "bot", None):
                return False  # bot çalışmıyor

            # Mevcut loop var mı kontrol et
            loop = self.bot_loop
            if loop and loop.is_running():
                asyncio.run_coroutine_threadsafe(
                    app.bot.send_message(chat_id=config.AUTHORIZED_CHAT_ID, text=text),
                    loop
                )
                return True
            else:
                return False

        except Exception as e:
            if config.ENABLE_LOGGING:
                self.logger.error(f"Mesaj gönderilemedi: {e}")
            return False

    # ---------- Yetki kontrol ----------
    def check_authorization(self, update: Update) -> bool:
        chat_id = update.effective_chat.id
        if chat_id != config.AUTHORIZED_CHAT_ID:
            if config.ENABLE_LOGGING:
                self.logger.warning(f"Yetkisiz erişim denemesi: Chat ID {chat_id}")
            return False
        return True

    # ---------- Komut işleyicileri ----------
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self.check_authorization(update):
            await update.message.reply_text(config.ERROR_MESSAGES["unauthorized"])
            if self.gui_callback:
                self.gui_callback("KOMUT", f"{update.message.text} komutu çalıştırıldı.")
            return
        await update.message.reply_text(config.WELCOME_MESSAGE, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self.check_authorization(update):
            await update.message.reply_text(config.ERROR_MESSAGES["unauthorized"])
            if self.gui_callback:
                self.gui_callback("KOMUT", f"{update.message.text} komutu çalıştırılamadı.")
            return
        await update.message.reply_text("📡 Sistem bilgileri alınıyor...")
        status_message = self.system.get_system_status()
        await update.message.reply_text(status_message, parse_mode='Markdown')
    
    async def screenshot_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self.check_authorization(update):
            await update.message.reply_text(config.ERROR_MESSAGES["unauthorized"])
            return
        await update.message.reply_text("📸 Ekran görüntüsü alınıyor...")
        screenshot_path = self.system.take_screenshot()
        if screenshot_path:
            with open(screenshot_path, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption="✅ Ekran görüntüsü alındı")
                if self.gui_callback:
                    self.gui_callback("KOMUT", f"{update.message.text} komutu çalıştırıldı.")
        else:
            await update.message.reply_text("❌ Ekran görüntüsü alınamadı")
            if self.gui_callback:
                self.gui_callback("KOMUT", f"{update.message.text} komutu çalıştırılamadı.")

    async def webcam_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/kameragoruntu - Bağlı webcam'den tek kare gönderir"""
        if not self.check_authorization(update):
            await update.message.reply_text(config.ERROR_MESSAGES["unauthorized"])
            return
        await update.message.reply_text("📷 Kamera görüntüsü alınıyor...")
        path = self.system.take_webcam_shot()
        if path:
            with open(path, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption="📸 Webcam görüntüsü")
                if self.gui_callback:
                    self.gui_callback("KOMUT", f"{update.message.text} komutu çalıştırıldı.")
        else:
            await update.message.reply_text("⚠️ Kamera bağlı değil veya görüntü alınamadı.")
            if self.gui_callback:
                self.gui_callback("KOMUT", f"{update.message.text} komutu çalıştırılamadı. Kamera yok")
    
    async def shutdown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self.check_authorization(update):
            await update.message.reply_text(config.ERROR_MESSAGES["unauthorized"])
            return
        success, message = self.system.shutdown_system()
        await update.message.reply_text(message)
    
    async def logout_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self.check_authorization(update):
            await update.message.reply_text(config.ERROR_MESSAGES["unauthorized"])
            return
        success, message = self.system.logout_session()
        await update.message.reply_text(message)
        if self.gui_callback:
                self.gui_callback("KOMUT", f"{update.message.text} komutu çalıştırıldı.")

    async def post_init(self, application: Application):
        """Bot başlatıldığında çalışır ve bildirim gönderir"""
        try:
            node_name = platform.node()
            
            msg = (
                f"🚀 *PC Controller Başlatıldı*\n\n"
                f"🖥️ *Bilgisayar:* `{node_name}`\n"
                f"🕒 *Zaman:* {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
                f"Bot komut almaya hazır! ✅"
            )
            
            await application.bot.send_message(
                chat_id=config.AUTHORIZED_CHAT_ID,
                text=msg,
                parse_mode='Markdown'
            )
        except Exception as e:
            if config.ENABLE_LOGGING:
                self.logger.error(f"Başlangıç mesajı gönderilemedi: {e}")

    # ---------- Bot Başlat ----------
    def run(self):
        """Botu başlatır ve ayrı thread'de çalıştırır."""
        if not config.BOT_TOKEN or config.BOT_TOKEN == "BURAYA_BOT_TOKEN_YAZIN":
            print(config.ERROR_MESSAGES["config_error"])
            return None
        if config.AUTHORIZED_CHAT_ID == 0:
            print("⚠️ UYARI: AUTHORIZED_CHAT_ID ayarlanmamış!")
            return None

        self.application = Application.builder().token(config.BOT_TOKEN).post_init(self.post_init).build()

        # Komutlar
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("pcdurum", self.status_command))
        self.application.add_handler(CommandHandler("ekrangoruntu", self.screenshot_command))
        self.application.add_handler(CommandHandler("kameragoruntu", self.webcam_command))
        self.application.add_handler(CommandHandler("pckapat", self.shutdown_command))
        self.application.add_handler(CommandHandler("otorumkapat", self.logout_command))

        # Serbest metin mesajları (sohbet için)
        async def any_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            try:
                msg_text = update.message.text if update.message else None
                if msg_text and self.check_authorization(update):
                    if self.gui_callback:
                        self.gui_callback("Telegram", msg_text)
                elif not self.check_authorization(update):
                    await update.message.reply_text(config.ERROR_MESSAGES["unauthorized"])
            except Exception as e:
                if config.ENABLE_LOGGING:
                    self.logger.error(f"Mesaj işleme hatası: {e}")

        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, any_text_handler))

        # Thread başlatma
        def _run():
            self.bot_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.bot_loop)
            print("✅ Bot başlatıldı ve mesaj bekliyor...")
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)

        t = threading.Thread(target=_run, daemon=True)
        t.start()

        return self.application
