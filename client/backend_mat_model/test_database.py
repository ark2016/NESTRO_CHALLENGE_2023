from database import basa



base=basa("localhost","web","web00top","hack")
base.conect_to_database() #соедение с базой
#print(base.print_all_rows("trunks")) # вывод строк таблицы
#base.add_new_trunk('trunks','A-B', 56, 8.6, 8.6, 8.6, 8.6, 7.6, 'анйный', 10, 15, 36, 16,29) #добавление строки
#print(base.print_all_rows("trunks")) # вывод строк таблицы
base.add_new_trunk('trunks','000', 56, 8.6, 8.6, 8.6, 8.6, 7.6, 'анйный', 10, 15, 36, 16,2)
print(base.get_trunk('trunks','000'))
base.disconect_database() # отсоедение от базы