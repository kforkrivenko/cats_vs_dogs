# -*- coding: utf-8 -*-

import telebot
import sqlite3
import image_working
import predicting_category

# Создаем экземпляр бота
bot = telebot.TeleBot('6693987412:AAEi10qIn5scHrkXNyyzBGMh0-f_YPyvSnI')

# Создание базы данных SQLite
conn = sqlite3.connect('../local_storage/example.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''DROP TABLE IF EXISTS images''')
cursor.execute('''CREATE TABLE IF NOT EXISTS images
                (id INTEGER,
                photo BLOB,
                number INTEGER)''')
cursor.execute("INSERT INTO images (id, number) VALUES (?, ?)",
               (0, 0))
conn.commit()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне изображение.")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # -*- coding: utf-8 -*-

    import telebot
    import sqlite3
    import image_working
    import predicting_category

    # Создаем экземпляр бота
    bot = telebot.TeleBot('6693987412:AAEi10qIn5scHrkXNyyzBGMh0-f_YPyvSnI')

    # Создание базы данных SQLite
    conn = sqlite3.connect('/root/telegram_bot/local_storage/example.db', check_same_thread=False)
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute('''DROP TABLE IF EXISTS images''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS images
                    (id INTEGER,
                    photo BLOB,
                    number INTEGER)''')
    cursor.execute("INSERT INTO images (id, number) VALUES (?, ?)",
                   (0, 0))
    conn.commit()

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Привет! Отправь мне изображение.")

    @bot.message_handler(content_types=['photo', 'document'])
    def handle_photo(message):
        if message.content_type == 'document':
            # Получаем информацию о фото
            file_id = message.document.file_id

            # Загружаем фото с использованием file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Сохраняем фото на сервере
            scr = f'../local_storage/{message.chat.id}/' + message.document.file_name
            with open(scr, 'wb') as new_file:
                new_file.write(downloaded_file)

            image_working.insert_blob(message.chat.id, scr)

            prediction = predicting_category.predict(scr)

            bot.reply_to(message, f'Перед нами {prediction}')
        elif message.content_type == 'photo':
            # Получаем информацию о фото

            # Загружаем фото с использованием file_id
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Сохраняем фото на сервере
            scr = f'../local_storage/{message.chat.id}/' + message.document.file_name
            with open(scr, 'wb') as new_file:
                new_file.write(downloaded_file)

            image_working.insert_blob(message.chat.id, scr)

            prediction = predicting_category.predict(scr)

            bot.reply_to(message, f'Перед нами {prediction}')

    # Запускаем бота
    bot.polling()


# Запускаем бота
bot.polling()
