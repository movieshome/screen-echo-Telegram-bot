import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hi! Send me a video to update the caption.")

# Video handler
async def handle_video(update: Update, context: CallbackContext):
    if update.message.video:  # Check if the message contains a video
        context.user_data['video'] = update.message.video.file_id
        context.user_data['original_caption'] = update.message.caption or "No caption provided."
        await update.message.reply_text(
            "Got your video. Reply with the new caption or type /default to use the default caption."
        )

# Reply handler
async def handle_reply(update: Update, context: CallbackContext):
    video_file_id = context.user_data.get('video')  # Retrieve saved video file_id
    if not video_file_id:  # If no video has been sent yet
        await update.message.reply_text("No video found. Please send a video first.")
        return

    new_caption = update.message.text.strip()  # Get the new caption

    # Send the video back with the new caption
    await update.message.reply_video(
        video=video_file_id,
        caption=new_caption,
        parse_mode="Markdown"
    )
    # Clear stored video after use
    context.user_data.clear()

# Default command handler
async def handle_default(update: Update, context: CallbackContext):
    video_file_id = context.user_data.get('video')  # Retrieve saved video file_id
    if not video_file_id:  # If no video has been sent yet
        await update.message.reply_text("No video found. Please send a video first.")
        return

    # Default caption
    default_caption = "@ScreenEcho\nThis movie is provided by ScreeEcho\nhttps://screenecho.blogspot.com/"

    # Send the video back with the default caption
    await update.message.reply_video(
        video=video_file_id,
        caption=default_caption,
        parse_mode="Markdown"
    )
    # Clear stored video after use
    context.user_data.clear()

# Main function
def main():
    TOKEN = "8019873611:AAF5fdTK5iosBX72CcqKpUVU769FTaxVHXw"  # Your bot token
    application = Application.builder().token(TOKEN).build()

    # Add handler for /start command
    application.add_handler(CommandHandler("start", start))
    # Add handler for video messages
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    # Add handler for text replies
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply))
    # Add handler for /default command
    application.add_handler(CommandHandler("default", handle_default))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
