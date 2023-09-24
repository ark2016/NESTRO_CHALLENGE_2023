import random
import numpy as np
# import backend_mat_model.data
from backend_mat_model.data import *
import json

name = "C2/D2-I3/E"
d = 426
t_n = 16.4
length = 2970
P_start = 1.88
P_finish = 1.46
param_charge = 40
param_Qn = [2714, 2352, 2472, 2933, 2568, 1641, 1398, 2626, 1788, 1362]
param_Qg = [0]*10
param_Qv = param_Qn
t_k = [random.uniform(13, 16.4) for k in range(100)]
t_cp = np.mean(t_k)
sigma = standard_deviation_sigma(100, t_k, t_cp)
t_min = minimum_possible_wall_thickness(t_cp, sigma, t_k, increased_accuracy=True)
v_cp = average_corrosion_rate_of_pipeline_wall(t_n, t_min, 10)
param_lifetime = residual_life_of_pipeline(t_min, 10, v_cp)
param_critic_velocity_param_factic_velocity = critical_drift_speed(2650, 997, 2*10**5, 0.8, d*10**(-3))
param_P = average_pressure_in_area(P_start, P_finish)
param_T = None
param_flow_regime = None
transition = None
param_crash = None
param_critic_velocity = None

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
    "transition": transition,
    "param_crash": param_crash,
    "param_critic_velocity": param_critic_velocity,
    "param_lifetime": param_lifetime
}
print(dictionary)
# Serializing json
# json_object = json.dumps(dictionary, indent=4)
