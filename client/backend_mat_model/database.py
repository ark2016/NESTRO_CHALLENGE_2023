"""

import mysql.connector

from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user=input("Имя пользователя: "),
        password=getpass("Пароль: "),
    ) as connection:
        print(connection)
except Error as e:
    print(e)

    python. / setup.py
    install

"""