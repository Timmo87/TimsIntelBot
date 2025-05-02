import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

saved_messages = {}

BOT_NAME = "Tim’s Intel Bot"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Привет! Я {BOT_NAME}. Я буду сохранять твои медиафайлы. "
        "Чтобы скачать медиа — ответь на сообщение с фото или видео."
    )

async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    replied = message.reply_to_message

    if replied:
        if replied.photo:
            file = await replied.photo[-1].get_file()
            await file.download_to_drive()
            await update.message.reply_text("Фото сохранено.")
        elif replied.video:
            file = await replied.video.get_file()
            await file.download_to_drive()
            await update.message.reply_text("Видео сохранено.")
        else:
            await update.message.reply_text("Ответьте на фото или видео.")
    else:
        await update.message.reply_text("Ответьте на сообщение с медиа.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, save_message))

    print(f"{BOT_NAME} запущен!")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())