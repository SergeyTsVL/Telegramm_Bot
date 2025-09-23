import random

with open('JOKES.csv', 'r', encoding='utf8') as file:
    random_number = random.randint(1, 25)
    a = 0
    for row in file:
        a += 1
        if a == random_number:
            print(row)


# bot.send_message(chat_id=chat_id, text=text)