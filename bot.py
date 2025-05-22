from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re, os

TOKEN = os.getenv("TOKEN")
URL_REGEX = r'(https?://[^\s]+)'

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 হ্যালো! আমি একটি লিংক ফিল্টার বট।\n"
        "✅ আপনি যদি কোনো ছবি বা ভিডিওর ক্যাপশনে লিংক পাঠান,\n"
        "তাহলে আমি শুধু লিংক আলাদা করে রিপ্লাই করব।\n\n"
        "📌 চেষ্টা করে দেখুন!"
    )

# Media + caption handler
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = update.message.caption
    if caption:
        links = re.findall(URL_REGEX, caption)
        if links:
            await update.message.reply_text("🔗 লিংক পাওয়া গেছে:
" + '\n'.join(links))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler((filters.PHOTO | filters.VIDEO) & filters.Caption(), handle_media))

    print("Bot is running...")
    app.run_polling()
