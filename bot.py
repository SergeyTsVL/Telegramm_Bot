import requests
import telebot
from PIL import Image, ImageOps
import io
from telebot import types
import os
import random

# Прописываю токен в свой пайчарм
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
user_states = {}  # тут будем хранить информацию о действиях пользователя
# набор символов из которых составляем изображение
ASCII_CHARS = '@%#*+=-:. '
SIZE = None

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    print(image)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def image_to_ascii(image_stream, new_width=40):
    # Переводим в оттенки серого
    image = Image.open(image_stream).convert('L')
    # меняем размер сохраняя отношение сторон
    width, height = image.size
    aspect_ratio = height / float(width)
    new_height = int(
        aspect_ratio * new_width * 0.55)  # 0,55 так как буквы выше чем шире
    img_resized = image.resize((new_width, new_height))
    img_str = pixels_to_ascii(img_resized)
    img_width = img_resized.width
    max_characters = 4000 - (new_width + 1)
    max_rows = max_characters // (new_width + 1)
    ascii_art = ""
    for i in range(0, min(max_rows * img_width, len(img_str)), img_width):
        ascii_art += img_str[i:i + img_width] + "\n"
    return ascii_art

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
    return characters

def pixelate_image(image, pixel_size):
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    return image

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f"Пришлите мне изображение, и я предложу вам варианты!\n"
                          f"Не забывай - {random_compliment(message)}",
                 reply_markup=get_options_keyboard_0())   # добавляем кнопку для вывода шуток
    # bot.reply_to(message, random_compliment(message))

def get_options_keyboard_0():
    """
    Добавляем кнопку для вывода случайных шуток из списка файла JOKES.csv
    :return:
    """
    keyboard = types.InlineKeyboardMarkup()
    random_Joke_btn = types.InlineKeyboardButton("Random Joke", callback_data="random_Joke")
    keyboard.add(random_Joke_btn)
    return keyboard

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "Я получил вашу фотографию! Пожалуйста, выберите, что вы хотели бы с ней сделать.\n"
                          "Вы можете использовать свои собственные символы в формате ASCII, просто отправьте ими "
                          "сообщение.",
                 reply_markup=get_options_keyboard())
    user_states[message.chat.id] = {'photo': message.photo[-1].file_id}

def get_options_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    pixelate_btn = types.InlineKeyboardButton("Pixelate", callback_data="pixelate")
    ascii_btn = types.InlineKeyboardButton("ASCII Art", callback_data="ascii")
    invert_btn = types.InlineKeyboardButton("Invert colors", callback_data="invert")
    reflected_btn = types.InlineKeyboardButton("Reflected image", callback_data="reflected")
    heatmap_btn = types.InlineKeyboardButton("Convert to heatmap", callback_data="heatmap")
    size_btn = types.InlineKeyboardButton("Size", callback_data="change_size")
    random_Joke_btn = types.InlineKeyboardButton("Random Joke", callback_data="random_Joke")
    keyboard.add(pixelate_btn, ascii_btn, invert_btn, reflected_btn, heatmap_btn, size_btn, random_Joke_btn)
    return keyboard

@bot.message_handler(content_types=['text'])
def text_processing(message):
    global ASCII_CHARS
    global SIZE
    if 'размер' in message.text:
        SIZE = str(message.text)
        a = 0
        for i in SIZE:
            a += 1
            if a < 7:
                SIZE = SIZE.replace(SIZE[0], "")
        SIZE = int(SIZE) or 128
    else:
        CHARACTER_SET = str(message.text)
        ASCII_CHARS = CHARACTER_SET or '@%#*+=-:. '
        ascii_and_send(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pixelate":
        bot.answer_callback_query(call.id, "Пикселизация вашего изображения...")
        pixelate_and_send(call.message)
        bot.send_message(call.message.chat.id, f'{random_compliment(call.message.chat.id)}')
    elif call.data == "ascii":
        bot.answer_callback_query(call.id, "Преобразование вашего изображения в формат ASCII art...")
        ascii_and_send(call.message)
        bot.send_message(call.message.chat.id, f'{random_compliment(call.message.chat.id)}')
    elif call.data == "invert":
        bot.answer_callback_query(call.id, "Преобразование вашего изображения в обратное...")
        invert_colors(call.message)
        bot.send_message(call.message.chat.id, f'{random_compliment(call.message.chat.id)}')
    elif call.data == "reflected":
        bot.answer_callback_query(call.id, "Преобразование вашего отраженного изображения...")
        reflected_image(call.message)
        bot.send_message(call.message.chat.id, f'{random_compliment(call.message.chat.id)}')
    elif call.data == "heatmap":
        bot.answer_callback_query(call.id, "Преобразование тепловой карты вашего изображения...")
        convert_to_heatmap(call.message)
        bot.send_message(call.message.chat.id, f'{random_compliment(call.message.chat.id)}')
    elif call.data == "random_Joke":
        bot.answer_callback_query(call.id, "Внимание сейчас будет сгенерирована шутка программиста...")
        bot.send_message(call.message.chat.id, f'{random_joke(call.message.chat.id)}')
    elif call.data == "change_size":
        bot.answer_callback_query(call.id, "Преобразование размера вашего изображения...")
        # Проверяем есть ли фото в наличии
        if call.message.json['reply_to_message']['photo'][-1]['file_id']:  # да... структура зависит от версии пайтона
            # Получаем информацию о файле
            file_info = bot.get_file(call.message.json['reply_to_message']['photo'][-1]['file_id'])
            file_path = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
            try:
                # Загружаем и изменяем изображение
                response = requests.get(file_path)
                response.raise_for_status()
                image_stream = response.content
                image = Image.open(io.BytesIO(image_stream))
                resized_image = resize_for_sticker(image, SIZE)
                # Сохраняем измененное изображение в поток
                buffer = io.BytesIO()
                resized_image.save(buffer, format='JPEG')
                buffer.seek(0)
                # Отправляем измененное изображение обратно в Telegram
                bot.send_photo(
                    chat_id=call.message.chat.id,
                    photo=buffer,
                    caption="Измененное изображение"
                )
                bot.send_message(call.message.chat.id, f'{random_compliment(call.message.chat.id)}')
            except Exception as e:
                bot.answer_callback_query(call.id, f"Произошла ошибка: {str(e)}")
        else:
            bot.answer_callback_query(call.id, "В этом сообщении не найдено ни одной фотографии.")

def pixelate_and_send(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    pixelated = pixelate_image(image, 20)

    output_stream = io.BytesIO()
    pixelated.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(message.chat.id, output_stream)

def ascii_and_send(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)
    ascii_art = image_to_ascii(image_stream)
    bot.send_message(message.chat.id, f"```\n{ascii_art}\n```", parse_mode="MarkdownV2")

def invert_colors(message):
    """
    Инвертирует цвета изображения, для этого сначала считывает изображение, обрабатывает его и отправляет уже
    обработанное обратно в чат.
    :param message:
    :return:
    """
    photo_id = user_states[message.chat.id]['photo']  # Обозначаем какое изображение будем обрабатывать.
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)   # Обрабатываем изображение
    inverted_image = ImageOps.invert(image)
    output_stream = io.BytesIO()   # Отправляем изображение обратно в чат
    inverted_image.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(message.chat.id, output_stream)
    return inverted_image

def reflected_image(message):
    """
    Зеркально отражает изображение, для этого сначала считывает изображение, обрабатывает его и отправляет уже
    обработанное обратно в чат.
    :param message:
    :return:
    """
    photo_id = user_states[message.chat.id]['photo']  # Обозначаем какое изображение будем обрабатывать.
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream).convert("L")
    reflected_image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    output_stream = io.BytesIO()   # Отправляем изображение обратно в чат
    reflected_image.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(message.chat.id, output_stream)
    return reflected_image

def convert_to_heatmap(message):
    """
    Создает тепловое изображение в градиенте белый черный, для этого сначала считывает изображение, обрабатывает его и отправляет уже
    обработанное обратно в чат.
    :param message:
    :return:
    """
    photo_id = user_states[message.chat.id]['photo']  # Обозначаем какое изображение будем обрабатывать.
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream).convert("L")
    heatmap_image = ImageOps.colorize(image, black="blue", white="white")
    output_stream = io.BytesIO()   # Отправляем изображение обратно в чат
    heatmap_image.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(message.chat.id, output_stream)
    return heatmap_image

def resize_for_sticker(image, max_size=SIZE):
    """
    Изменение размера фото до указанного как SIZE.
    Примерный ввод размера в для отправки сообщением: "размер 128"
    """
    # Получаем текущие размеры изображения
    width, height = image.size
    # Определяем новые размеры, сохраняя пропорции
    if width > height:
        new_width = max_size
        new_height = int(height * max_size / width)
    else:
        new_height = max_size
        new_width = int(width * max_size / height)
    # Создаем новое изображение с заданными размерами
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    return resized_image

def random_joke(message):
    """
    Генерируем случайные шутки из списка шуток файла формата .csv
    :param message:
    :return:
    """
    with open('JOKES.csv', 'r', encoding='utf8') as file:
        random_number = random.randint(1, 25)
        a = 0
        for row in file:
            a += 1
            if a == random_number:
                return row

def random_compliment(message):
    """
    Генерируем случайные шутки из списка шуток файла формата .csv
    :param message:
    :return:
    """
    with open('COMPLIMENTS.csv', 'r', encoding='utf8') as file:
        random_number = random.randint(1, 25)
        a = 0
        for row in file:
            a += 1
            if a == random_number:
                return row
bot.polling(none_stop=True)
