
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import os

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

saved_messages = {}

BOT_NAME = "Tim’s Intel Bot"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Привет! Я {BOT_NAME}. Я буду сохранять удалённые сообщения и медиа. "
        "Чтобы скачать медиа — ответь на фото или видео любым сообщением."
    )

async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    chat_id = message.chat_id
    message_id = message.message_id

    content = message.text or message.caption or "[Медиа]"
    saved_messages[(chat_id, message_id)] = message

    logging.info(f"Сохранили сообщение {message_id} в чате {chat_id}: {content[:50]}")

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message and message.reply_to_message:
        replied = message.reply_to_message

        if replied.photo:
            file = await replied.photo[-1].get_file()
            await file.download_to_drive("saved_photo.jpg")
            await update.message.reply_text("Фото скачано.")
        elif replied.video:
            file = await replied.video.get_file()
            await file.download_to_drive("saved_video.mp4")
            await update.message.reply_text("Видео скачано.")
        else:
            await update.message.reply_text("Ответьте на фото или видео!")
    else:
        await update.message.reply_text("Пожалуйста, ответьте на медиа, чтобы скачать.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, save_message))
    app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, download_media))
    print(f"{BOT_NAME} запущен!")
    await app.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()