import os
import sqlite3
import telebot

# Создаем бота
# Прописываю токен в свой пайчарм
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
# Список для хранения слов
words_list = []

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Введите первое слово:")
    bot.register_next_step_handler(message, get_first_word)

def get_first_word(message):
    first_word = message.text
    words_list.append(first_word)
    bot.send_message(message.chat.id, "Введите второе слово:")
    bot.register_next_step_handler(message, get_second_word)

def get_second_word(message):
    second_word = message.text
    words_list.append(second_word)
    bot.send_message(message.chat.id, f"Слова добавлены: {words_list}")

# Запуск бота
bot.polling()