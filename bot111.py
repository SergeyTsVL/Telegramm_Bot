import json
import sqlite3

import telebot
from PIL import Image, ImageOps
import io
from telebot import types
import os
import random
import requests
from io import BytesIO

# from probe import bot
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
# Прописываю токен в свой пайчарм


table_names_list = []
messages_list = []


# Состояния
WAITING_FOR_CATEGORY = 'waiting_for_category'
WAITING_FOR_row = 'waiting_for_row'

# Хранение состояний пользователей
user_states = {}
user_states_row = {}

list_table = []
a = 0



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



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    global list_table
    if call.data == "create_category":
        bot.send_message(call.message.chat.id, 'Введи название новой категории')
        user_states[call.message.chat.id] = WAITING_FOR_CATEGORY
        list_table = []
    table_names = print_table_names()

    if call.data == "All_categories":
        list_table = []

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
    global a
    for table in table_names:
        if call.data == table:
            if table != 'sqlite_sequence':
                # print(call.data)
                # get_all_users(table)
                users = get_all_users(table, call.message)
                # print(users)
                keyboard = types.InlineKeyboardMarkup()  # Создаем клавиатуру один раз

                button = types.InlineKeyboardButton(text='Добавить задание',
                                                    callback_data='Добавить задание')  # Создаем кнопку для каждой таблицы

                keyboard.add(button)  # Добавляем кнопку в клавиатуру
                list_table.append(table)
                bot.send_message(call.message.chat.id, f"Категория '{table}' добавить задание ",
                                 reply_markup=keyboard)

                if users:
                    keyboard = types.InlineKeyboardMarkup()  # Создаем клавиатуру один раз
                    for row in users:
                        print(row)
                        if row[4] == 'не_выполнено':
                            button1 = types.InlineKeyboardButton(text='Редактирование',
                                                                callback_data=row[2])  # Создаем кнопку для каждой таблицы

                            button2 = types.InlineKeyboardButton(text='Выполнено',
                                                                callback_data=row[0])  # Создаем кнопку для каждой таблицы
                            keyboard.add(button1, button2)  # Добавляем кнопку в клавиатуру

                        else:

                            a += 1
                            keyboard.add(button)
                    bot.send_message(call.message.chat.id, f"Задание: {row[2]},\nдедлайн {row[3]},\nстатус '{row[4]}'",
                                     reply_markup=keyboard)

                    return keyboard
                        # response += f"ID: {row[0]}, Name: {row[1]}"

                    a = 0
                else:
                    list_table.append(table)



                    # keyboard = types.InlineKeyboardMarkup()  # Создаем клавиатуру один раз
                    #
                    # button = types.InlineKeyboardButton(text='Добавить задание',
                    #                                     callback_data='Добавить задание')  # Создаем кнопку для каждой таблицы
                    #
                    # keyboard.add(button)  # Добавляем кнопку в клавиатуру
                    # bot.send_message(call.message.chat.id, f"Категория '{table}' не имеет заданий ",
                    #                  reply_markup=keyboard)


    if call.data == "Добавить задание":
        bot.send_message(call.message.chat.id, 'Введи название новой строки "business"///"created_at"\n'
                                               'через ///\nПример: Разработать микросервис на FastAPI///20.10.25')
        user_states_row[call.message.chat.id] = WAITING_FOR_row
    print(call.data, 'print(call.data)')
    try:
        if [int(call.data)] in range(0, 300):
            print(call.data, 'call.data')
            update_row(call.message, call.data)
    except:
        None

def update_row(message, int_call):
    print(message, 'message')
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(f'''UPDATE [{list_table[0]}] SET data = ? WHERE id = ?''',
              ('Выполнено', int_call))
    print(int_call)
    # Сохраняем изменения в базе данных
    conn.commit()








def get_all_users(table, message):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    try:
        c.execute(f"SELECT * FROM {table}")
        rows = c.fetchall()
        return rows
    except:
        None
        # bot.reply_to(message, text='55555555')
    conn.close()
    # return rows



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

@bot.message_handler(
    func=lambda message: message.chat.id in user_states and user_states[message.chat.id] == WAITING_FOR_CATEGORY)
def handle_new_category(message):
    category_name = message.text
    # Здесь вы можете сохранить категорию в базе данных или выполнить другие действия
    bot.send_message(message.chat.id, f'Категория "{category_name}" успешно создана!')
    # Удаляем состояние пользователя
    del user_states[message.chat.id]
    f_create_category(category_name)

@bot.message_handler(
    func=lambda message: message.chat.id in user_states_row and user_states_row[message.chat.id] == WAITING_FOR_row)
def handle_new_row(message):
    print(message)
    row_name = message.text
    list_row = message.text.split('///')

    # Здесь вы можете сохранить категорию в базе данных или выполнить другие действия
    bot.send_message(message.chat.id, f'Запись в колонке business-> "{list_row[0]}" и created_at-> "{list_row[1]}" '
                                      f'успешно создана!')
    # Удаляем состояние пользователя
    create_business(message)
    del user_states_row[message.chat.id]

def create_business(message):
    list_row = message.text.split('///')
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(f'''
    INSERT INTO [{list_table[0]}] (id, username, business, created_at)
    VALUES (?, ?, ?, ?)
    ''', (message.from_user.id, message.from_user.username, list_row[0], list_row[1]))
    # Сохраняем изменения в базе данных
    conn.commit()



@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, f"Вы написали: {message.text}")

    return message.text

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


bot.polling()

