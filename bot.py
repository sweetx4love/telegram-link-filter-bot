from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import re, os

TOKEN = os.getenv("7753792475:AAGewlbt8QNw8mGNWcgnvAdKr_BEPa5cqm8")
URL_REGEX = r'(https?://[^\s]+)'

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = update.message.caption
    if caption:
        links = re.findall(URL_REGEX, caption)
        if links:
            # শুধু reply করবে, মূল মেসেজ অপরিবর্তিত থাকবে
            await update.message.reply_text('\n'.join(links))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    # ছবি বা ভিডিও ক্যাপশন আছে এমন সবকিছুতে কাজ করবে
    app.add_handler(MessageHandler((filters.PHOTO | filters.VIDEO) & filters.Caption(), handle_media))
    print("Bot is running...")
    app.run_polling()
