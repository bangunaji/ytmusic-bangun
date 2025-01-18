import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# Ganti dengan token bot Telegram kamu
TELEGRAM_TOKEN = '7682174100:AAECsd6jzA2RMgPO8k5lBkl-GJsGHAn-67g'

# Fungsi untuk memulai bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Halo! Kirimkan judul lagu atau link YouTube, dan saya akan mengirimkan link musiknya!")

# Fungsi untuk mencari musik di YouTube
async def search_song(update: Update, context: CallbackContext):
    search_query = ' '.join(context.args)
    if not search_query:
        await update.message.reply_text("Tolong berikan judul lagu atau link YouTube.")
        return

    # Gunakan yt-dlp untuk mencari video di YouTube
    ydl_opts = {
        'quiet': True,
        'extractaudio': True,
        'audioquality': 1,
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch:{search_query}", download=True)
        video_url = result['entries'][0]['url']
        audio_file = f"downloads/{result['entries'][0]['id']}.mp3"
        
        # Kirim file audio ke pengguna
        if os.path.exists(audio_file):
            await update.message.reply_audio(open(audio_file, 'rb'))
        else:
            await update.message.reply_text(f"Berikut adalah link video YouTube yang kamu cari: {video_url}")

# Fungsi untuk memulai bot dan mendaftarkan handler
def main():
    # Setup Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Daftarkan handler untuk perintah start dan search
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('search', search_song))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_song))  # Mendengarkan pesan teks tanpa perintah

    # Mulai bot
    application.run_polling()

if __name__ == '__main__':
    main()
