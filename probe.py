import os
import sqlite3
import telebot

# Создаем бота
# Прописываю токен в свой пайчарм
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)


# Подключение к базе данных (или создание новой, если она не существует)
conn = sqlite3.connect('example1.db')
cursor = conn.cursor()

# Создание таблицы users, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    message TEXT
)
''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Напиши мне что-нибудь, и я сохраню это в базе данных.")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Сохраняем данные в базу данных
    conn = sqlite3.connect('example1.db')
    cursor = conn.cursor()

    # Вставляем данные в таблицу
    cursor.execute('INSERT INTO users (username, message) VALUES (?, ?)', (message.from_user.username, message.text))
    # cursor.execute('UPDATE users SET message = ? WHERE user_id = ?', (message.text, user_id))
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, "Ваше сообщение сохранено!")


bot.polling()