# -*- coding: utf-8 -*-
import telebot
import predicting_category
from dotenv import load_dotenv
import os

# Создаем экземпляр бота (токен скрыт)
load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет! Отправь мне изображение и я определю что это - собака или кошка. Я пока маленький, меня обучали только на 500 изображениях")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Получаем информацию о фото
        # Загружаем фото с использованием file_id
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Сохраняем фото на сервере
        scr = f'/root/telegram_bot/local_storage/{message.chat.id}/photo'
        os.makedirs(os.path.dirname(scr), exist_ok=True)
        with open(scr, 'wb') as new_file:
            new_file.write(downloaded_file)

        prediction = predicting_category.predict(scr)

        bot.reply_to(message, f'Перед нами {prediction}')
    except Exception as err:
        bot.reply_to(message, 'Простите, произошла ошибка. Возможно вы отправили изображение как файл')
        file = open("errors.txt", "w")
        file.write(f'{err}')
        file.close()


# Запускаем бота
bot.polling()