import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder
application = ApplicationBuilder().token(TELEGRAM_TOKEN).connect_timeout(10).read_timeout(10).build()

# Token bot Telegram Anda
TELEGRAM_TOKEN = '7682174100:AAECsd6jzA2RMgPO8k5lBkl-GJsGHAn-67g'

# Fungsi untuk menangani perintah /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Halo! Kirimkan judul lagu atau link YouTube, dan saya akan membantu mencarikan musiknya!")

# Fungsi untuk menangani pencarian lagu
async def search_song(update: Update, context: CallbackContext):
    await update.message.reply_text("Fungsi pencarian lagu sedang dalam pengembangan.")

# Fungsi utama untuk menjalankan aplikasi
def main():
    # Inisialisasi aplikasi Telegram
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Tambahkan handler untuk perintah dan pesan teks
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_song))

    # Jalankan bot menggunakan polling
    application.run_polling()

if __name__ == '__main__':
    main()
