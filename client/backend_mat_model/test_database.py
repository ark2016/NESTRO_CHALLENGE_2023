from database import basa



base=basa("localhost","web","web00top","hack")
base.conect_to_database() #соедение с базой
#print(base.print_all_rows("trunks")) # вывод строк таблицы
#base.add_new_trunk('trunks','A-B', 56, 8.6, 8.6, 8.6, 8.6, 7.6, 'анйный', 10, 15, 36, 16,29) #добавление строки
#print(base.print_all_rows("trunks")) # вывод строк таблицы
#base.add_new_trunk('00', 56, 8.6, 8.6, 8.6, 8.6, 7.6, 'анйный', 10, 15, 36, 16,2)
print(base.get_trunk('00'))
base.disconect_database() # отсоедение от базы


"""
Как установить mysql?

Здесь все подробно описано
https://proglib.io/p/python-i-mysql-prakticheskoe-vvedenie-2021-01-06



Надо выполнить несколько SQL команд
Хорошая новость, для этого есть метод custom_command(comand)
Ниже нужные команды

Как создать базу данных?

create database hack;

Как создать нужную таблицу?

create table trunks
(
    id                  int auto_increment
        primary key,
    Model               varchar(100) not null,
    ParamCharge         int          not null,
    ParamQn             float        not null,
    ParamQg             float        not null,
    ParamQv             float        not null,
    P                   float        not null,
    T                   float        not null,
    ParamFlowRegime     varchar(100) not null,
    ParamFacticVelocity int          not null,
    ParamCriticVelocity int          not null,
    ParamCrash          int          not null,
    ParamLifetime       int          not null,
    ResidualResource    int          not null,
    Created             datetime     not null
);



"""