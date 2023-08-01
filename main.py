import telebot
import sqlite3
import image_working
import predicting_category

# Создаем экземпляр бота
bot = telebot.TeleBot('6693987412:AAEi10qIn5scHrkXNyyzBGMh0-f_YPyvSnI')

# Создание базы данных SQLite
conn = sqlite3.connect('example.db', check_same_thread=False)
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
    # Получаем информацию о фото
    photo = message.photo[-1]
    file_id = photo.file_id

    # Загружаем фото с использованием file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Сохраняем фото на сервере
    with open('photo.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)

    image_working.insert_blob(message.chat.id, "photo.jpg")

    # Предсказываем категорию
    image_path = 'photo.jpg'
    prediction = predicting_category.predict(image_path)

    bot.reply_to(message, f'Перед нами {prediction}')


# Запускаем бота
bot.polling()
