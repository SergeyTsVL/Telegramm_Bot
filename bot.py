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

table_names_list = []

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

# Состояния
WAITING_FOR_CATEGORY = 'waiting_for_category'

# Хранение состояний пользователей
user_states = {}


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "create_category":
        bot.send_message(call.message.chat.id, 'Введи название новой категории')
        user_states[call.message.chat.id] = WAITING_FOR_CATEGORY
    table_names = print_table_names()

    if call.data == "All_categories":

        table_names = print_table_names()
        if not table_names:
            bot.send_message(call.message.chat.id, "Нет таблиц в базе данных.")
            return
        keyboard = types.InlineKeyboardMarkup()  # Создаем клавиатуру один раз
        for table in table_names:
            if table != 'sqlite_sequence':
                table_names_list.append(table)
                button = types.InlineKeyboardButton(text=table, callback_data=table)  # Создаем кнопку для каждой таблицы
                keyboard.add(button)  # Добавляем кнопку в клавиатуру
        bot.send_message(call.message.chat.id, "Выберите таблицу:", reply_markup=keyboard)
        return keyboard

    for table in table_names:
        if call.data == table:
            print(call.data)
            # get_all_users(table)
            users = get_all_users(table)
            print(users)
            if users:
                response = "Список пользователей:\n"
                for user in users:
                    response += f"ID: {user[0]}, Name: {user[1]}"
            else:
                response = "Пользователи не найдены."

            bot.reply_to(call.message, response)

def get_all_users(table):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table}")
    rows = c.fetchall()
    conn.close()
    return rows



# @bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    # Получаем имя таблицы из callback_data
    table_name = call.data
    print(table_name)
    # Здесь вы можете вызвать нужную функцию, передав имя таблицы
    process_table(table_name, call)

def process_table(table_name, call):
    # Здесь вы можете выполнить нужные действия с таблицей
    bot.send_message(call.message.chat.id, f'Вы выбрали таблицу: {table_name}')




# def fff():
#     table_names = print_table_names()
#     print(table_names)
#     keyboard = types.InlineKeyboardMarkup()  # Создаем клавиатуру один раз
#     for table in table_names:
#         button = types.InlineKeyboardButton(text=table, callback_data=table)  # Создаем кнопку для каждой таблицы
#         keyboard.add(button)  # Добавляем кнопку в клавиатуру
#     return keyboard

            # markup.add(table)

        # bot.send_message(call.message.chat.id, "Выберите таблицу:", reply_markup=markup)



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

def print_table_names():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(f'''SELECT name FROM sqlite_master WHERE type='table'; ''')
    tables = c.fetchall()
    # Сохраняем изменения в базе данных
    conn.commit()
    return [table[0] for table in tables]




bot.polling(none_stop=True)