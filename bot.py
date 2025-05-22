from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re
import os

TOKEN = os.getenv("TOKEN") or "YOUR_BOT_TOKEN_HERE"
URL_REGEX = r'(https?://[^\s]+)'

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ চ্যানেল পোস্ট থেকে শুধু লিংক রেখে মিডিয়া রিপোস্ট হবে!")

# চ্যানেল পোস্ট হ্যান্ডলার
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = update.channel_post.caption
    if caption:
        links = re.findall(URL_REGEX, caption)
        if links:
            link_only = "\n".join(links)

            # যদি ছবি থাকে
            if update.channel_post.photo:
                file_id = update.channel_post.photo[-1].file_id
                await context.bot.send_photo(
                    chat_id=update.channel_post.chat_id,
                    photo=file_id,
                    caption=link_only
                )
            # যদি ভিডিও থাকে
            elif update.channel_post.video:
                file_id = update.channel_post.video.file_id
                await context.bot.send_video(
                    chat_id=update.channel_post.chat_id,
                    video=file_id,
                    caption=link_only
                )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & filters.ChatType.CHANNEL, handle_channel_post))

    print("✅ Bot is running...")
    app.run_polling()
