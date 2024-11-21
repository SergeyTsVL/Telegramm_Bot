# from PIL import Image
#
# img = Image.open("cats.png")
#
# # Задаем новый размер
# new_size = (800, 600)
#
# # Вычисляем коэффициент масштабирования
# scale_factor = min(new_size[0] / img.size[0], new_size[1] / img.size[1])
#
# # Вычисляем новые размеры с сохранением пропорций
# new_width = int(img.size[0] * scale_factor)
# new_height = int(img.size[1] * scale_factor)
#
# # Изменяем размер изображения
# img = img.resize((new_width, new_height))
#
# # Создаем новое изображение нужного размера и заполняем его белым цветом
# result_img = Image.new(img.mode, new_size, (255, 255, 255))
# result_img.paste(img, ((new_size[0] - new_width) // 2, (new_size[1] - new_height) // 2))
#
# # Сохраняем результат
# result_img.save("resized_with_padding.png")


#
# from telebot import TeleBot
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#
# # Создаем экземпляр бота
# bot = TeleBot('YOUR_BOT_TOKEN')
#
# # Создаем клавиатуру с кнопками
# keyboard = InlineKeyboardMarkup()
# button_yes = InlineKeyboardButton(text='Да', callback_data='yes')
# button_no = InlineKeyboardButton(text='Нет', callback_data='no')
# keyboard.add(button_yes, button_no)
#
# # Функция для обработки нажатия кнопок
# def handle_callback(call):
#     if call.data == 'yes':
#         bot.answer_callback_query(call.id, text="Вы выбрали Да")
#         bot.send_message(call.message.chat.id, "Спасибо за ответ!")
#     elif call.data == 'no':
#         bot.answer_callback_query(call.id, text="Вы выбрали Нет")
#         bot.send_message(call.message.chat.id, "Понятно, продолжайте!")
#
# # Обработчик сообщений
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id,
#                      "Привет! Выберите один из вариантов:",
#                      reply_markup=keyboard)
#
# # Запускаем обработку нажатий кнопок
# bot.set_my_commands(['/start'])
#
# # Запускаем бота
# bot.polling(none_stop=True)

from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import telebot

# Создаем экземпляр бота
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Создаем клавиатуру с кнопками
keyboard = InlineKeyboardMarkup()
button_large = InlineKeyboardButton(text='Большой', callback_data='large')
button_medium = InlineKeyboardButton(text='Средний', callback_data='medium')
button_small = InlineKeyboardButton(text='Маленький', callback_data='small')
keyboard.add(button_large, button_medium, button_small)


# Обработчик нажатия кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # Получаем размер стикера из callback_data
    sticker_size = call.data

    # Отправляем сообщение с результатом выбора
    bot.answer_callback_query(call.id, text="Вы выбрали размер стикера")

    # Отправляем сообщение с результатом выбора и информацией о размере
    bot.send_message(call.message.chat.id,
                     f"Вы выбрали {sticker_size} размер стикера",
                     reply_markup=types.ReplyKeyboardRemove())


# Функция для отправки начального сообщения с клавиатурой
def send_start_message():
    bot.send_message(bot.get_updates()[0].message.chat.id,
                     "Выберите размер стикера:",
                     reply_markup=keyboard)


# Запускаем бота
bot.polling(none_stop=True)