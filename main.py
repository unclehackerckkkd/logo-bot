
from telegram.ext import Updater, MessageHandler, Filters
from PIL import Image
import os
from io import BytesIO

from keep_alive import keep_alive  # استدعاء الوظيفة

# توكن البوت الجديد ✅
TOKEN = "8280782593:AAGS1Bul76qol2mCZwtvbXyVkax7j82mPYA"

def process_image(input_image):
    base_image = input_image.convert("RGBA")

    logo = Image.open("logo.png").convert("RGBA")
    logo = logo.resize(base_image.size)

    alpha = logo.split()[3]
    alpha = alpha.point(lambda p: p * 0.3)
    logo.putalpha(alpha)

    blended = Image.alpha_composite(base_image, logo)

    output = BytesIO()
    blended.convert("RGB").save(output, format="JPEG")
    output.seek(0)
    return output

def handle_photo(update, context):
    photo_file = update.message.photo[-1].get_file()
    photo_bytes = BytesIO()
    photo_file.download(out=photo_bytes)
    photo_bytes.seek(0)

    input_image = Image.open(photo_bytes)
    result_image = process_image(input_image)

    update.message.reply_photo(photo=result_image, caption="✅ تم تطبيق اللوجو")

def main():
    keep_alive()  # <-- هذا هو المفتاح لتشغيل دائم
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
