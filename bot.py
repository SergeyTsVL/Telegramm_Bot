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

# Прописываю токен в свой пайчарм
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

table_names_list = []
messages_list = []


# Состояния
WAITING_FOR_CATEGORY = 'waiting_for_category'
WAITING_FOR_row = 'waiting_for_row'

# Хранение состояний пользователей
user_states = {}
user_states_row = {}

list_table = []

# Список для хранения слов
words_list = []

int_call_data = []


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
    all_category = types.InlineKeyboardButton("Все категории", callback_data="All_categories")
    keyboard.add(create_category, all_category)
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
        if not table_names:
            bot.send_message(call.message.chat.id, "Нет таблиц в базе данных.")
            return
        keyboard14 = types.InlineKeyboardMarkup()  # Создаем клавиатуру один раз
        for table in table_names:
            if table != 'sqlite_sequence':
                table_names_list.append(table)
                button123 = types.InlineKeyboardButton(text=table, callback_data=table)  # Создаем кнопку для каждой таблицы
                keyboard14.add(button123)  # Добавляем кнопку в клавиатуру
        bot.send_message(call.message.chat.id, "Выберите категорию:", reply_markup=keyboard14)
        # print(call.message)
        return keyboard14

    for table in table_names:
        # print(table)

        if call.data == table:
            if table != 'sqlite_sequence':
                list_table.append(table)
                # get_all_users(table)
                users = get_all_users(table, call.message)
                keyboard1 = types.InlineKeyboardMarkup()  # Создаем клавиатуру один раз

                button11 = types.InlineKeyboardButton(text='Добавить задание',
                                                    callback_data='data_work')  # Создаем кнопку для каждой таблицы

                keyboard1.add(button11)  # Добавляем кнопку в клавиатуру
                bot.send_message(call.message.chat.id, f"Категория '{table}' не имеет заданий ",
                                 reply_markup=keyboard1)
                if users:
                    keyboard = types.InlineKeyboardMarkup()  # Создаем клавиатуру один раз
                    d = []
                    dd = []
                    aa = 0
                    for row in users:
                        # aa += 1
                        # print(row)
                        # if 'button' not in d and 'button1' not in d:
                        if row[0] not in d:
                            d.append(row[0])
                            print(row[0], " if 'button' not in d and 'button1' not in d:")
                            # keyboard = types.InlineKeyboardMarkup()  # Создаем клавиатуру один раз
                            button = types.InlineKeyboardButton(text='Редактирование',
                                                                callback_data=f'++{row[0]}')  # Создаем кнопку для каждой таблицы

                            button1 = types.InlineKeyboardButton(text='Выполнено',
                                                                 callback_data=f'{row[0]}')  # Создаем кнопку для каждой таблицы

                        # if 'button' not in dd and 'button1' not in dd:
                        #     dd.append('button')
                        #     dd.append('button1')
                        #     dd.append(keyboard.add(button, button1))
                            keyboard.add(button, button1)  # Добавляем кнопку в клавиатуру
                            print(keyboard)

                        # d += 1
                        if row[4] == 'не_выполнено':
                            # try:
                            bot.send_message(call.message.chat.id, f"Категория '{list_table[0]}',\nЗадание: {row[2]},\nДедлайн {row[3]},\nСтатус '{row[4]}'",
                                             reply_markup=keyboard)
                            aa += 1
                            #     None
                        else:
                            bot.send_message(call.message.chat.id,
                                             f"Категория '{list_table[0]}',\nЗадание: {row[2]},\nДедлайн {row[3]},\nСтатус '{row[4]}'")
                            # d = []
                            None

                    return keyboard
                        # response += f"ID: {row[0]}, Name: {row[1]}"
                else:
                    # keyboard = types.InlineKeyboardMarkup()  # Создаем клавиатуру один раз
                    #
                    # button = types.InlineKeyboardButton(text='Добавить задание',
                    #                                     callback_data='Добавить задание')  # Создаем кнопку для каждой таблицы
                    #
                    # keyboard.add(button)  # Добавляем кнопку в клавиатуру
                    list_table.append(table)
    # bot.send_message(call.message.chat.id, f'После нажатия кнопки перезапустите отправив сообщение старт /start ')



    if call.data == "data_work":
        bot.send_message(call.message.chat.id, 'Введи название новой строки "business"///"created_at"\n'
                                               'через ///\nПример: Разработать микросервис на FastAPI///20.10.25')
        user_states_row[call.message.chat.id] = WAITING_FOR_row

    try:
        if int(call.data) in range(0, 100000000000, 1):
            # print(call.data, 'call.data')
            done_row(call.data)
            # bot.send_message(call.message.chat.id, f'После нажатия кнопки перезапустите отправив сообщение старт /start ')
    except:
        None

    try:
        if int(call.data[2:]) in range(0, 100000000000, 1) and call.data[:2] == '++':
            int_call_data.append(call.data[2:])
            start_message(call.message)

            # bot.send_message(call.message.chat.id, f'После нажатия кнопки перезапустите отправив сообщение старт /start ')
    except:
        None

# def update_row(int_call_data, call_message):
    # # bot.send_message(call_message.chat.id, "Введите первое слово business:")
    # # bot.register_next_step_handler(call_message, get_first_word)
    # #
    # # first_word = call_message.text
    # # words_list.append(first_word)
    # # bot.send_message(call_message.chat.id, "Введите второе слово:")
    # # bot.register_next_step_handler(call_message, get_second_word)
    # start_message()
    #
    # global list_table, words_list
    # print(list_table[0])
    # print(words_list[0])
    # print(words_list[1])
    # conn = sqlite3.connect('example.db')
    # c = conn.cursor()
    # c.execute(f'''UPDATE [{list_table[0]}] SET business = ? created_at = ? WHERE id = ?''',
    #           (words_list[0], words_list[1], int(int_call_data)))
    # # Сохраняем изменения в базе данных
    # conn.commit()
#
def start_message(message):
    bot.send_message(message.chat.id, "Введите первое слово:")
    bot.register_next_step_handler(message, get_first_word)

def get_first_word(message):
    first_word = message.text
    words_list.append(first_word)
    bot.send_message(message.chat.id, "Введите описание задания:")
    bot.register_next_step_handler(message, get_second_word)
#
def get_second_word(message):
    second_word = message.text
    words_list.append(second_word)
    bot.send_message(message.chat.id, f"Введите дату выполнения задания: {words_list}")
    try:
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        global int_call_data
        x = str(words_list[0])
        y = str(words_list[1])
        z = int(int_call_data[0])
        c.execute(f'''UPDATE [{list_table[0]}] SET business = ?, created_at = ? WHERE id = ?''', (x, y, z))
        # Сохраняем изменения в базе данных
        conn.commit()
    except:
        None
    finally:
        conn.close()

    # global int_call_data
    int_call_data = []








def done_row(int_call):
    print(list_table[0])
    print(int_call)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(f'''UPDATE [{list_table[0]}] SET data = ? WHERE id = ?''',
              ('Выполнено', int(int_call)))
    # Сохраняем изменения в базе данных
    conn.commit()






def get_all_users(table, message):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    try:
        c.execute(f"SELECT id, username, business, created_at, data FROM {table}")
        rows = c.fetchall()
        # print(rows)
        return rows
    except:
        None
        # bot.reply_to(message, text='55555555')
    conn.close()




# @bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    # Получаем имя таблицы из callback_data
    table_name = call.data
    # print(table_name)
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
    # bot.send_message(message.chat.id, 'Можно прописывать задание на добавление данных в строку')
    # print(message['from_user'])
    # message = json.loads(message)
    # print(message.from_user.username)
    # print(message.from_user.id)
    list_row = message.text.split('///')
    # print(list_row)




    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute(f'''
    INSERT INTO [{list_table[0]}] (username, business, created_at)
    VALUES (?, ?, ?)
    ''', (message.from_user.username, list_row[0], list_row[1]))
    # Сохраняем изменения в базе данных
    conn.commit()
    # bot.send_message(message.chat.id, f'После нажатия кнопки перезапустите отправив сообщение старт /start ')

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
            created_at TEXT,
            data TEXT DEFAULT 'не_выполнено'
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

