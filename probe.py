import sqlite3

import telebot
from PIL import Image, ImageOps
import io
from telebot import types
import os
import random
import requests
from io import BytesIO

# Прописываю токен в свой пайчарм
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f"Посмотрите актуальный список задач ",
                 reply_markup=get_options_keyboard_0())   # добавляем кнопки для вывода и ввода данных
def get_options_keyboard_0():
    """
    Добавляем кнопку для вывода случайных шуток из списка файла JOKES.csv
    :return:
    """
    keyboard = types.InlineKeyboardMarkup()
    create_category= types.InlineKeyboardButton("Создать категорию", callback_data="create_category")
    list_business = types.InlineKeyboardButton("Список дел", callback_data="To-do_list")
    all_category = types.InlineKeyboardButton("Все категории", callback_data="All_categories")
    keyboard.add(create_category, list_business, all_category)
    return keyboard
#
#
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, f"Вы написали 1111111: {message.text}")
#
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     if call.data == "create_category":
#         bot.send_message(call.message.chat.id, f'Введи название новой категории')
#         # как здесь прописать что я хочу ввести новую категорию в сообщении к боту
#
#         bot.reply_to(call.message, f"Вы написали: {call.message.text}")
#         echo_message(call.message)
#         print(call.message.json)

# Состояния
WAITING_FOR_CATEGORY = 'waiting_for_category'

# Хранение состояний пользователей
user_states = {}


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "create_category":
        bot.send_message(call.message.chat.id, 'Введи название новой категории')
        user_states[call.message.chat.id] = WAITING_FOR_CATEGORY


@bot.message_handler(
    func=lambda message: message.chat.id in user_states and user_states[message.chat.id] == WAITING_FOR_CATEGORY)
def handle_new_category(message):
    category_name = message.text
    # Здесь вы можете сохранить категорию в базе данных или выполнить другие действия
    bot.send_message(message.chat.id, f'Категория "{category_name}" успешно создана!')

    # Удаляем состояние пользователя
    del user_states[message.chat.id]
    f_create_category(category_name)
    # return category_name


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, f"Вы написали: {message.text}")






def f_create_category(message):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS [{message}] (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,          
            business TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            data TEXT DEFAULT не_выполнено
        )
    ''')
    # Сохраняем изменения в базе данных
    conn.commit()
    pass




bot.polling(none_stop=True)