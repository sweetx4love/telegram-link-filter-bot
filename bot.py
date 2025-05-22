from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re
import os

TOKEN = os.getenv("TOKEN")  # অথবা সরাসরি 'YOUR_BOT_TOKEN'

URL_REGEX = r'(https?://[^\s]+)'

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📢 শুধু লিংক রেখে বাকি ক্যাপশন রিমুভ করে মিডিয়া রিপোস্ট করা হবে!"
    )

# মিডিয়া হ্যান্ডলার
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = update.message.caption
    if caption:
        links = re.findall(URL_REGEX, caption)
        if links:
            link_only = '\n'.join(links)

            # ফটো
            if update.message.photo:
                file_id = update.message.photo[-1].file_id
                await update.message.reply_photo(photo=file_id, caption=link_only)

            # ভিডিও
            elif update.message.video:
                file_id = update.message.video.file_id
                await update.message.reply_video(video=file_id, caption=link_only)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        (filters.PHOTO | filters.VIDEO) & filters.Caption(), handle_media
    ))

    print("✅ Bot is running...")
    app.run_polling()
