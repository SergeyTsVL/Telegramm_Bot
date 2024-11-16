# from PIL import Image, ImageOps
#
# # Открываем изображение
# image = Image.open("input_image.jpg")
#
# # Инвертируем изображение
# inverted_image = ImageOps.invert(image)
#
# # Сохраняем инвертированное изображение
# inverted_image.save("output_inverted_image.jpg")
#
# # Выводим оригинальное и инвертированное изображения
# image.show(title="Оригинал")
# inverted_image.show(title="Инвертированное")

import logging
from telegram import Update, ForceReply, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

logging.basicConfig(level=logging.INFO)

TOKEN = 'YOUR_BOT_TOKEN'


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Запустить функцию", callback_data='run_function')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Привет! Нажми кнопку, чтобы запустить функцию.', reply_markup=reply_markup)


def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "run_function":
        run_my_function(context, query)


def run_my_function(context, query):
    # Ваш код здесь
    result = some_complex_calculation()
    query.edit_message_text(f"Результат: {result}")


def some_complex_calculation():
    # Пример сложного вычисления
    return sum(range(1000000))


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(callback_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
