import os
import io
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from rembg import remove
from PIL import Image

TOKEN = os.getenv("8516027704:AAF3ymGkX_X0YIjIDDrRT_fc6kEK-anw0iE")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً 👋\nأرسل صورة وسأعيدها لك بدون خلفية 😊"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("⏳ جاري معالجة الصورة…")

        photo_file = await update.message.photo[-1].get_file()
        img_bytes = await photo_file.download_as_bytearray()

        input_image = Image.open(io.BytesIO(img_bytes))
        output_image = remove(input_image)

        output_bytes = io.BytesIO()
        output_image.save(output_bytes, format="PNG")
        output_bytes.seek(0)

        await update.message.reply_document(
            document=output_bytes,
            filename="no_bg.png",
            caption="تمت إزالة الخلفية ✅"
        )

    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()