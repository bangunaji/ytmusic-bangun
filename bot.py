import logging
from telegram.ext import ApplicationBuilder, CommandHandler

# Setup logging
logging.basicConfig(level=logging.INFO)

async def start(update, context):
    await update.message.reply_text("Halo! Bot ini berjalan dengan baik.")

def main():
    logging.info("Bot is starting...")

    # Inisialisasi aplikasi Telegram
    application = ApplicationBuilder().token('7682174100:AAECsd6jzA2RMgPO8k5lBkl-GJsGHAn-67g').build()

    # Tambahkan handler untuk perintah /start
    application.add_handler(CommandHandler('start', start))

    # Jalankan bot menggunakan polling
    application.run_polling()

if __name__ == '__main__':
    main()
