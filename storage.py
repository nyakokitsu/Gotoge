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
    sqlite_create_table_users_query = '''CREATE TABLE users (
                                uid INTEGER NOT NULL UNIQUE,
                                ref TEXT,
                                added_at datetime);'''
    cursor.execute(sqlite_create_table_query)
    cursor.execute(sqlite_create_table_users_query)
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

def create_user(telegram_id: int, ref: str = "") -> list[str]:
    """
    Сохраняет юзера

    :param telegram_id: ID юзера в Telegram
    :return:
    """
    insert_data = f"""INSERT INTO users (uid, ref, added_at) VALUES ({telegram_id}, '{ref}', '{datetime.datetime.now()}');"""
    try:
        cursor.executescript(insert_data)
        sqlite_connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def is_user_already_exists(telegram_id: int) -> bool:
    """
    Проверяет существование пользователя

    :param telegram_id: ID юзера в Telegram
    :return:
    """
    
    sqlite_select_query = """SELECT (uid) from users where uid = {}"""
    cursor.execute(sqlite_select_query.format(telegram_id))
    records = cursor.fetchall()
    #print("Всего строк:  ", len(records))
    if len(records) > 0:
        return True
    else:
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
    #print("Всего строк:  ", len(records))
    results = []
    for row in records:
        results.append(row[1])
    return results

"""
def users_migr():
    select = "SELECT DISTINCT (uid) FROM gotoge;"
    cursor.execute(select)
    records = cursor.fetchall()
    for rec in records:
        insert_data = f"INSERT INTO users (uid, ref, added_at) VALUES ({rec[0]}, '', '{datetime.datetime.now()}');"
        cursor.executescript(insert_data)
        sqlite_connection.commit()
"""


def delete_image(telegram_id: int, photo_file_unique_id: str) -> bool:
    """
    Удаляет изображение

    :param telegram_id: ID юзера в Telegram
    :param photo_file_unique_id: file_unique_id изображения для удаления
    """
    sqlite_select_query = """DELETE from gotoge WHERE uid = {} AND photo_unique_id = '{}'"""
    cursor.execute(sqlite_select_query.format(telegram_id, photo_file_unique_id))
    sqlite_connection.commit()

