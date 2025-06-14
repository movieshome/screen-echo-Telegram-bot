import os
from telegram.ext import ApplicationBuilder, CommandHandler

# Get token from environment variable (set this in Pella dashboard)
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("Hello! I'm alive and running!")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

if __name__ == '__main__':
    app.run_polling()
