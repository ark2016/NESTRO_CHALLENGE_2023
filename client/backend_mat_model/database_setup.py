from database import basa
import getpass
from mysql.connector import connect, Error

user=input("user: ")
password= getpass.getpass()
#base=basa("localhost",user,password,"hack")
connection = connect(
                host="localhost",
                user=user,
                password=password,
            )

try:
    cursor = connection.cursor()
    data="create database hack;"
    cursor.execute(data)
    connection.commit()
    print("Успешное создание базы " + "hack")
except Error as e:
    print(e)

try:
    cursor = connection.cursor()
    data="""
    GRANT SELECT, INSERT, UPDATE ON hack.* TO 'web'@'localhost';
    ALTER USER 'web'@'localhost' IDENTIFIED BY 'web00top';
"""
    cursor.execute(data)
    connection.commit()
    print("Успешное добавление пользователя web ")
except Error as e:
    print(e)

try:
    cursor = connection.cursor()
    data="""
    create table trunks
(
    id                  int auto_increment
        primary key,
    Model               varchar(100) not null,
    ParamCharge         float        not null,
    ParamQn             float        not null,
    ParamQg             varchar(100) not null,
    ParamQv             float        not null,
    P                   float        not null,
    T                   float        not null,
    ParamFlowRegime     varchar(100) not null,
    ParamFacticVelocity float        not null,
    ParamCriticVelocity float        not null,
    ParamCrash          float        not null,
    ParamLifetime       float        not null,
    ResidualResource    float        not null,
    Created             datetime     not null
);
    """
    cursor.execute(data)
    connection.commit()
    print("Успешное создание таблицы " + "trunks")
except Error as e:
    print(e)

