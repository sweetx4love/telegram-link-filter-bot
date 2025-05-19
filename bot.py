from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import re, os

# Bot token env থেকে
TOKEN = os.getenv("TOKEN")

URL_REGEX = r'(https?://[^\s]+)'

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = update.message.caption
    if caption:
        links = re.findall(URL_REGEX, caption)
        if links:
            await update.message.reply_text('\n'.join(links))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO & filters.Caption(), handle_photo))
    print("Bot is running...")
    app.run_polling()
