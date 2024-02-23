from typing import Optional
import sqlite3
import datetime

sqlite_connection = sqlite3.connect('database.db')
cursor = sqlite_connection.cursor()


def init_db():
    sqlite_select_query = "select sqlite_version();"
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
    print("[LOG] SQLite version: ", record)
    sqlite_create_table_query = '''CREATE TABLE gotoge (
                                uid INTEGER,
                                photo_file_id TEXT NOT NULL,
                                photo_unique_id text NOT NULL UNIQUE,
                                added_at datetime);'''
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()


def close_connection():
    cursor.close()
    sqlite_connection.close()

def add_photo(
        telegram_id: int,
        photo_file_id: str,
        photo_unique_id: str
):
    """
    Сохраняет изображение в словарь

    :param telegram_id: ID юзера в Telegram
    :param photo_file_id: file_id изображения
    :param photo_unique_id: file_unique_id изображения
    """
    insert_data = f"""INSERT INTO gotoge (uid, photo_file_id, photo_unique_id, added_at)
    VALUES ({telegram_id}, '{photo_file_id}', '{photo_unique_id}', '{datetime.datetime.now()}');"""
    try:
        cursor.executescript(insert_data)
        sqlite_connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False



def get_images_by_id(telegram_id: int) -> list[str]:
    """
    Получает сохранённые изображения пользователя

    :param telegram_id: ID юзера в Telegram
    :return:
    """
    
    sqlite_select_query = """SELECT * from gotoge where uid = {}"""
    cursor.execute(sqlite_select_query.format(telegram_id))
    records = cursor.fetchall()
    print("Всего строк:  ", len(records))
    results = []
    for row in records:
        results.append(row[1])
    return results


def delete_link(telegram_id: int, link: str):
    """
    Удаляет ссылку

    :param telegram_id: ID юзера в Telegram
    :param link: ссылка
    """
    if telegram_id in data:
        if "links" in data[telegram_id]:
            if link in data[telegram_id]["links"]:
                del data[telegram_id]["links"][link]


def delete_image(telegram_id: int, photo_file_unique_id: str):
    """
    Удаляет изображение

    :param telegram_id: ID юзера в Telegram
    :param photo_file_unique_id: file_unique_id изображения для удаления
    """
    if telegram_id in data and "images" in data[telegram_id]:
        for index, (_, unique_id) in enumerate(data[telegram_id]["images"]):
            if unique_id == photo_file_unique_id:
                data[telegram_id]["images"].pop(index)

