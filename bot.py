import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters
import os

# Token bot Telegram Anda
TELEGRAM_TOKEN = '7682174100:AAECsd6jzA2RMgPO8k5lBkl-GJsGHAn-67g'

# Fungsi untuk menangani perintah /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Halo! Kirimkan judul lagu atau link YouTube, dan saya akan membantu mencarikan musiknya!")

# Fungsi untuk mengunduh audio dari YouTube
def download_audio_from_youtube(url):
    ydl_opts = {
        'format': 'bestaudio/best',  # Mengambil format audio terbaik
        'outtmpl': 'downloaded_song.%(ext)s',  # Nama file keluaran
        'postprocessors': [{
            'key': 'FFmpegAudio',
            'preferredcodec': 'mp3',  # Format mp3
            'preferredquality': '192',  # Kualitas audio
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Fungsi untuk menangani pencarian dan pengiriman musik
async def search_song(update: Update, context: CallbackContext):
    query = update.message.text  # Mendapatkan pesan dari user
    if "youtube.com" in query:
        # Jika link YouTube dikirim, coba unduh audio
        await update.message.reply_text("Mengunduh musik dari YouTube, harap tunggu...")
        download_audio_from_youtube(query)
        music_file = 'downloaded_song.mp3'  # Nama file yang diunduh
        await update.message.reply_audio(open(music_file, 'rb'))
        os.remove(music_file)  # Hapus file setelah dikirim
    else:
        await update.message.reply_text("Fungsi pencarian lagu sedang dalam pengembangan. Silakan kirimkan link YouTube.")

# Fungsi utama untuk menjalankan aplikasi
def main():
    # Inisialisasi aplikasi Telegram
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Tambahkan handler untuk perintah dan pesan teks
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_song))

    # Jalankan bot menggunakan polling
    application.run_polling()

if __name__ == '__main__':
    main()
