import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters
)
from googleapiclient.discovery import build

# Konfigurasi logging untuk debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Token bot Telegram Anda
TELEGRAM_TOKEN = '7682174100:AAECsd6jzA2RMgPO8k5lBkl-GJsGHAn-67g'

# API Key YouTube
YOUTUBE_API_KEY = 'AIzaSyC-2ai2bpanZTcLsYUXbW_uac0a7l8dL8A'  # Ganti dengan API Key YouTube Anda

# Fungsi untuk menangani perintah /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Halo! Kirimkan judul lagu atau link YouTube, dan saya akan membantu mencarikan musiknya!"
    )
    logger.info(f"User {update.effective_user.username} menjalankan perintah /start.")

# Fungsi untuk mencari lagu di YouTube
async def search_song(update: Update, context: CallbackContext):
    query = update.message.text  # Pesan dari pengguna
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    
    # Pencarian video di YouTube
    search_response = youtube.search().list(
        q=query, part="snippet", maxResults=1, type="video"
    ).execute()
    
    if search_response['items']:
        video = search_response['items'][0]
        video_title = video['snippet']['title']
        video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
        await update.message.reply_text(f"Judul: {video_title}\nLink: {video_url}")
    else:
        await update.message.reply_text("Maaf, tidak dapat menemukan lagu tersebut.")
    logger.info(f"Melakukan pencarian untuk: {query}")

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
