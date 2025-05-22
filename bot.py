from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re
import os

TOKEN = os.getenv("TOKEN")  # অথবা সরাসরি 'YOUR_BOT_TOKEN' দিয়ে দিন
URL_REGEX = r'(https?://[^\s]+)'

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 হ্যালো! ছবি বা ভিডিওর ক্যাপশনে যদি লিংক থাকে, আমি শুধু সেই লিংক রিপ্লাই করব!"
    )

# ক্যাপশন থেকে শুধু লিংক তুলে রেসপন্স
async def handle_media_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = update.message.caption
    if caption:
        links = re.findall(URL_REGEX, caption)
        if links:
            link_only = '\n'.join(links)
            # মিডিয়াকে touch না করে শুধু reply
            await update.message.reply_text(link_only)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # ফটো বা ভিডিও + ক্যাপশন এলে হ্যান্ডল করবে
    app.add_handler(MessageHandler(
        (filters.PHOTO | filters.VIDEO) & filters.Caption(),
        handle_media_caption
    ))

    print("✅ Bot is running...")
    app.run_polling()
