from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re, os

TOKEN = os.getenv("TOKEN")
URL_REGEX = r'(https?://[^\s]+)'

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """👋 হ্যালো! আমি একটি লিংক ফিল্টার বট।
✅ আপনি যদি কোনো ছবি বা ভিডিওর ক্যাপশনে লিংক পাঠান,
তাহলে আমি শুধু লিংক আলাদা করে রিপ্লাই করব।

📌 এখন চেষ্টা করে দেখুন!"""
    )

# মিডিয়া + ক্যাপশন হ্যান্ডলার
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = update.message.caption
    if caption:
        links = re.findall(URL_REGEX, caption)
        if links:
            # ইউজারের মিডিয়াকে touch না করে, শুধু reply করবে
            await update.message.reply_text("🔗 লিংক পাওয়া গেছে:\n" + '\n'.join(links))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # /start command
    app.add_handler(CommandHandler("start", start))

    # ফটো বা ভিডিও + ক্যাপশন আসলে handle করবে
    app.add_handler(MessageHandler((filters.PHOTO | filters.VIDEO) & filters.Caption(), handle_media))

    print("Bot is running...")
    app.run_polling()
