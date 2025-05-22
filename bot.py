from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re, os

# Replace with your bot token or set it as environment variable
TOKEN = os.getenv("TOKEN")
URL_REGEX = r'(https?://[^\s]+)'

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """👋 হ্যালো! আমি একটি লিংক ফিল্টার বট।
✅ আপনি যদি কোনো ছবি বা ভিডিওর ক্যাপশনে লিংক পাঠান,
আমি শুধু সেই লিংক আলাদা করে রিপ্লাই করব।

📌 এখন চেষ্টা করে দেখুন!"""
    )

# Handle media with caption
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = update.message.caption
    if caption:
        links = re.findall(URL_REGEX, caption)
        if links:
            # শুধু লিংক নিয়ে রিপ্লাই করবে, বাকি ক্যাপশন ignore
            only_links = '\n'.join(links)
            await update.message.reply_text(only_links)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler((filters.PHOTO | filters.VIDEO) & filters.Caption(), handle_media))

    print("✅ Bot is running...")
    app.run_polling()
