# Telegramm_Bot

# Многофункциональный телеграм-бот по адресу "@My_bot_is_a_robot".

## Описание

Данный бот умеет работать с фотографиями и преобразовывать их в ASCII-арт, Pixelate, Invert colors и др. 
Бот дорабатывается и добавляются свои функции.

## Основные функции

Описание функционала:

Импорты и настройки
- telebot используется для взаимодействия с Telegram API.
- PIL (Python Imaging Library), известная как Pillow, предоставляет инструменты для работы с изображениями.
- TOKEN — это строковая переменная, куда вы должны поместить токен вашего бота, полученный от @BotFather в Telegram.
- bot = telebot.TeleBot(TOKEN) создает экземпляр бота для взаимодействия с Telegram.
- TOKEN = os.environ.get("TOKEN") Закрепляет конфигурацию токена в PyCharm, как указано на рисунке.
![Uploading 1.png…](https://github.com/SergeyTsVL/Telegramm_Bot/blob/3.2/images/1.png)
![Uploading 1.png…](https://github.com/SergeyTsVL/Telegramm_Bot/blob/3.2/images/2.png)
Хранение состояний пользователей
- user_states используется для отслеживания действий или состояний пользователей. Например, какое изображение было отправлено.
Пикселизация
pixelate_image(image, pixel_size):
- Принимает изображение и размер пикселя. Уменьшает изображение до размера, где один пиксель представляет большую область, затем увеличивает обратно, создавая пиксельный эффект.
![Uploading 1.png…](https://github.com/SergeyTsVL/Telegramm_Bot/blob/3.2/images/3.png)
Преобразование в ASCII-арт
![Uploading 1.png…](https://github.com/SergeyTsVL/Telegramm_Bot/blob/3.2/images/4.png)
Подготовка изображения:
- resize_image(image, new_width=100): Изменяет размер изображения с сохранением пропорций.
- grayify(image): Преобразует цветное изображение в оттенки серого.
- image_to_ascii(image_stream, new_width=40): Основная функция для преобразования изображения в ASCII-арт. Изменяет размер, преобразует в градации серого и затем в строку ASCII-символов.
pixels_to_ascii(image):
![Uploading 1.png…](https://github.com/SergeyTsVL/Telegramm_Bot/blob/3.2/images/5.png)
Конвертирует пиксели изображения в градациях серого в строку ASCII-символов, используя предопределенную строку ASCII_CHARS.
![Uploading 1.png…](https://github.com/SergeyTsVL/Telegramm_Bot/blob/3.2/images/6.png)
![Uploading 1.png…](https://github.com/SergeyTsVL/Telegramm_Bot/blob/3.5/images/7.png)
![Uploading 1.png…](https://github.com/SergeyTsVL/Telegramm_Bot/blob/3.8/images/8.png)
![Uploading 1.png…](https://github.com/SergeyTsVL/Telegramm_Bot/blob/3.8/images/9.png)
Взаимодействие с пользователем
Обработчики сообщений:

- @bot.message_handler(commands=['start', 'help']): Реагирует на команды /start и /help, отправляя приветственное сообщение.
- @bot.message_handler(content_types=['photo']): Реагирует на изображения, отправляемые пользователем, и предлагает варианты обработки.
Клавиатура для взаимодействия:
- get_options_keyboard(): Создает клавиатуру с кнопками для выбора пользователем, как обработать изображение: через пикселизацию или преобразование в ASCII-арт.
Обработка запросов
Обработка колбэков:
- @bot.callback_query_handler(func=lambda call: True): Определяет действия в ответ на выбор пользователя (например, пикселизация или ASCII-арт) и вызывает соответствующую функцию обработки.
Отправка результатов
Функции отправки:
- pixelate_and_send(message): Пикселизирует изображение и отправляет его обратно пользователю.
- ascii_and_send(message): Преобразует изображение в ASCII-арт и отправляет результат в виде текстового сообщения.

