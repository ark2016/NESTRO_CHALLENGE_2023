from backend_mat_model.data import *
from backend_mat_model.database import *
import pandas as pd

df = pd.read_csv("Приложение 2. Данные о потоке нефти, газа и воды по каждому трубопроводу.xlsx - Данные для кейса.csv")

names = df['Наименование трубопровода']
diameter = df['Ø, мм']
thickness = df['Толщина стенки, мм']
length = df['Длина, м']
P_start = df['вход ']
P_end = df['выход ']
Q_n = df.iloc[:, 7:17]
V_l = df.iloc[:, 17:27]
W = df.iloc[:, 27:37]
Q_g = df.iloc[:, 37:47]
T_cp_n = df.iloc[:, 47:57]
T_cp_k = df.iloc[:, 57:67]
P_cp_n = df.iloc[:, 67:77]
P_cp_k = df.iloc[:, 77:87]


print(P_cp_k)
