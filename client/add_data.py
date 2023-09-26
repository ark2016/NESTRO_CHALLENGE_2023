from backend_mat_model.data import *
from backend_mat_model.database import *
import pandas as pd
import numpy as np
import json
import random

df = pd.read_csv("Приложение 2. Данные о потоке нефти, газа и воды по каждому трубопроводу.xlsx - Данные для кейса.csv")
df = df.fillna(0)

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

base=basa("localhost","web","web00top","hack")
base.conect_to_database() #соедение с базой

for i in range(len(names)):
    name = names[i]
    param_Qn = [Q_n.iloc[i, k] for k in range(len(Q_n.iloc[i]))]
    param_Qg = [Q_g.iloc[i, k] for k in range(len(Q_g.iloc[i]))]
    # param_Qv = [V_l.iloc[i, k] for k in range(len(V_l.iloc[i]))]
    param_Qv = param_Qn
    for i in range(len(param_Qn)):
        if type(param_Qv[i]) == "float" and type(param_Qg[i]) == "float":
            param_Qv[i] += param_Qg[i]
    # param_Qv = [j = (param_Qn[i] + param_Qg[i]) for i in range(len(param_Qn))]
    param_charge = [W.iloc[i, k] for k in range(len(W.iloc[i]))]  # мб то
    param_P = average_pressure_in_area(float(P_start[i].replace(",", ".")), float(P_end[i].replace(",", ".")))
    param_T = T_cp_n.iloc[i]
    param_flow_regime = ""
    param_critic_velocity = get_v_kr(nu_v, float(diameter[i].replace(",", ".")))  # заполнено?

    if existence_of_anti_corrosion_regime(mu_h=0.04 * 1000, n=20, D=float(diameter[i].replace(",", ".")), beta=0.2,
                                          ro_n=823, ro_v=997, mu_np=0.034, v_n=7.316, sigma=1):
        param_flow_regime += "антикоррозионный"
    else:
        param_flow_regime += "неантикоррозионный"

    t_k = [random.uniform(float(thickness[i].replace(",", ".")) - 5, float(thickness[i].replace(",", ".")))
           for k in range(100)]  # данные о замерах
    # sigma = standard_deviation_sigma(100, t_k, t_cp)
    param_critic_velocity_param_factic_velocity = dependence_of_critical_flow_velocity(sigma=25, ro_v=997, ro_n=823,
                                                                                       mu_n=0.04 * 1000, beta_b=0.2,
                                                                                       D=float(diameter[i]
                                                                                               .replace(",", ".")),
                                                                                       beta_in=0.3, mu_v=0.89)

    if param_critic_velocity > param_critic_velocity_param_factic_velocity:
        param_flow_regime += " ламинарный"
    else:
        param_flow_regime += "Турбулентный"

    param_crash = internal_pressure_pipeline_element_can_withstand(t_n=float(diameter[i].replace(",", ".")),
                                                                   delta_0=float(diameter[i].replace(",", ".")),
                                                                   delta=(np.mean(t_k) - float(thickness[i]
                                                                                               .replace(",", "."))),
                                                                   R_H_1=100, m2=0.6, k1=.8, alfa=1,
                                                                   D_n=float(diameter[i].replace(",", "."))
                                                                       + float(thickness[i].replace(",", ".")) * 2)
    # Вероятностный расчёт остаточного ресурса с учётом
    # общего коррозионно-зрозненного износа стенки труб
    t_cp = np.mean(t_k)
    sigma = standard_deviation_sigma(len(t_k), t_k, t_cp)
    t_min = minimum_possible_wall_thickness(t_cp, sigma, t_k, increased_accuracy=True)
    v_cp = average_corrosion_rate_of_pipeline_wall(float(thickness[i].replace(",", ".")), t_min, 10)
    param_lifetime = residual_life_of_pipeline(t_min,10, v_cp)  # годы

    base.add_new_trunk(name,
                       param_charge,
                       param_Qn,
                       param_Qg,
                       param_Qv,
                       param_P,
                       param_T,
                       param_flow_regime,
                       param_critic_velocity_param_factic_velocity,
                       param_critic_velocity,
                       param_crash,
                       param_lifetime,
                       0
                       )
    dictionary = {
        "name": name,
        "param_charge": param_charge,
        "param_Qn": param_Qn,
        "param_Qg": param_Qg,
        "param_Qv": param_Qv,
        "param_P": param_P,
        "param_T": param_T,
        "param_flow_regime": param_flow_regime,
        "param_critic_velocity_param_factic_velocity": param_critic_velocity_param_factic_velocity,
        "param_crash": param_crash,
        "param_critic_velocity": param_critic_velocity,
        "param_lifetime": param_lifetime
    }
    # json_object = json.dumps(dictionary, indent=4)
    # with open("example.json", "w") as outfile:
    #     outfile.write(json_object)


# print(len(P_cp_k.iloc[0]))

base.disconect_database() # отсоедение от базы
