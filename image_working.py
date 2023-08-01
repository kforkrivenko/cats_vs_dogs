import sqlite3


def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


# нужно еще try-except
def insert_blob(user_id, photo):
    # подключаемся к БД
    sqlite_connection = sqlite3.connect('example.db', check_same_thread=False)
    cursor = sqlite_connection.cursor()

    # Ищем последнюю запись
    cursor.execute('SELECT number FROM images ORDER BY number DESC LIMIT 1')
    new_number = cursor.fetchone()[0] + 1

    # Записываем в БД новую информацию
    sqlite_insert_blob_query = """INSERT INTO images
                                  (id, photo, number) VALUES (?, ?, ?)"""

    emp_photo = convert_to_binary_data(photo)
    # Преобразование данных в формат кортежа
    data_tuple = (user_id, emp_photo, new_number)
    cursor.execute(sqlite_insert_blob_query, data_tuple)
    sqlite_connection.commit()
    cursor.close()