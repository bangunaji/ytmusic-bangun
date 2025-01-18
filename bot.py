import asyncio
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters,
)

# Konfigurasi logging untuk debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Token bot Telegram Anda
TELEGRAM_TOKEN = '7682174100:AAECsd6jzA2RMgPO8k5lBkl-GJsGHAn-67g'

# Fungsi untuk menangani perintah /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Halo! Kirimkan judul lagu atau link YouTube, dan saya akan membantu mencarikan musiknya!"
    )
    logger.info(f"User {update.effective_user.username} menjalankan perintah /start.")

# Fungsi untuk menangani pencarian lagu
async def search_song(update: Update, context: CallbackContext):
    await update.message.reply_text("Fungsi pencarian lagu sedang dalam pengembangan.")
    logger.info(f"Pesan diterima: {update.message.text}")

# Fungsi utama untuk menjalankan aplikasi
def main():
    try:
        # Inisialisasi aplikasi Telegram
        application = (
            ApplicationBuilder()
            .token(TELEGRAM_TOKEN)
            .connect_timeout(30)  # Timeout koneksi (detik)
            .read_timeout(30)     # Timeout pembacaan respons (detik)
            .build()
        )

        # Tambahkan handler untuk perintah dan pesan teks
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_song))

        # Jalankan bot menggunakan polling
        logger.info("Bot sedang berjalan...")
        application.run_polling()

    except Exception as e:
        logger.error(f"Terjadi kesalahan: {e}")

if __name__ == '__main__':
    main()
