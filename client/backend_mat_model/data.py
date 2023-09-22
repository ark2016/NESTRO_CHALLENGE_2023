import pandas as pd
import numpy as np

# const
# (4.1-4.4)
n = 1.2
m1 = 0.8
m3 = 1

# (6.1)
k = 1


def conditionME075(R_H_1, R_H_2, m2, m3):
    return (R_H_2 * m3) / (R_H_1 * m2) >= .75


# ОСТ 153-39.4-010-2002 | 8 страница (4.1) (4.2)
def pipe_wall_thickness_for_decommissioning(R_H_1: float, R_H_2: float, P: float, alfa: float, D_h: float, k1: float,
                                            m2: float) -> float:
    """
    R1: расчётное сопротивление материала труб и деталей трубопровода, Па
    :param R_H_1: нормативное сопротивление, равное наименьшему значению пре менного сопротивления разрыву материала
    труб, принимаемое по ГОСТу или ТУ на соответствующие виды труб. Па
    :param R_H_2: нормативное сопротивление, равное наименьшему значению предела текучести при растяжении, сжатии и
    изгибе материала труб, принимаемое по ГОСТу или ТУ на соответствующие трубы. Па
    :param m2: коэффициент условий работы трубопровода, величина которого принимается в зависимости от транспортируемой
    фель для токсичных, горю чих, взрывоопасных и сжиженных газов 0,6; для инертных газов (ают, воздух и т.п.) или
    токсичных, горючих, взрывоопасных жидкостей 0,75; для инерт ных жидкостей 0.9:
    m3: кэффициент условий работы материала труб при повышенных тем пературах, для условий работы промысловых
    трубопроводов
    n: const
    :param P: рабочее давление в трубопроводе, Па
    :param alfa: коэффициент несущей способности, см. спецификацию
    :param D_h: наружный диаметр трубы или детали трубопровода, м
    m1: const
    :param k1: коэффициент однородности материала труб: для бесшовных труб из углеродистой и для сварных труб из
    низколегированной ненормализованной стали к 0,8, для сварных труб из углеродистой и для сварных труб из
    нормализованной низколегированной стали к, 0,85
    :return:толщина стенки трубы или детали трубопровода при которой они должны быть изъяты из
    эксплуатации, м
    """
    if conditionME075(R_H_1, R_H_2, m2, m3):
        R1 = R_H_1 * m1 * m2 * k1
        pipe_wall_thickness = (n * P * alfa * D_h) / (2 * (R1 + n * P))
    else:
        pipe_wall_thickness = (n * P * alfa * D_h) / (2 * (0.9 * R_H_2 * m3 + n * P))
    return pipe_wall_thickness


# допустимое давление ОСТ 153-39.4-010-2002 | 9 страница (4.3) (4.4)
def permissible_pressure_func(t: float, R_H_2: float, R_H_1: float, m2: float, alfa: float, D_n: float,
                              k1: float) -> float:
    """
    :param t: толщина стенки трубы, м (не указано)
    :param R_H_2: нормативное сопротивление, равное наименьшему значению предела текучести при растяжении, сжатии и
    изгибе материала труб, принимаемое по ГОСТу или ТУ на соответствующие трубы. Па
    :param R_H_1:нормативное сопротивление, равное наименьшему значению пре менного сопротивления разрыву материала
    труб, принимаемое по ГОСТу или ТУ на соответствующие виды труб. Па
    :param m2: коэффициент условий работы трубопровода, величина которого принимается в зависимости от транспортируемой
    фель для токсичных, горю чих, взрывоопасных и сжиженных газов 0,6; для инертных газов (ают, воздух и т.п.) или
    токсичных, горючих, взрывоопасных жидкостей 0,75; для инерт ных жидкостей 0.9:
    :param alfa: коэффициент несущей способности, см. спецификацию
    :param D_n: наружный диаметр трубы или детали трубопровода, м
    :param k1: коэффициент однородности материала труб: для бесшовных труб из углеродистой и для сварных труб из
    низколегированной ненормализованной стали к 0,8, для сварных труб из углеродистой и для сварных труб из
    нормализованной низколегированной стали к, 0,85
    :return: допустимое давление
    """
    if conditionME075(R_H_1, R_H_2, m2, m3):
        R1 = R_H_1 * m1 * m2 * k1
        permissible_pressure = (2 * t * R1) / (n * (alfa * D_n - 2 * t))
    else:
        permissible_pressure = (1.8 * R_H_2 * m3) / (n * (alfa * D_n - 2 * t))
    return permissible_pressure


# Расчёты напряжённо-деформированного состояния трубопроводов
# ОСТ 153-39.4-010-2002 | 16 страница (6,1) Проверочный расчет толщины стенки трубопровода, а также её
# определение в случае ремонта
def check_calculation_of_pipeline_wall_thickness(gamma_f: float, P: float, D_h: float,
                                                 contains_hydrogen_sulfide: bool, R_H_1: float, R_H_2: float,
                                                 m2: float, gamma_m: float, gamma_n: float, gamma_s: float) -> float:
    """
    :param gamma_f:
    k: коэффициент несущей способности труб и соединительных до талей, значение которого принимается согласно
    СП 34-116-97 (для труб, заглушек и переходов - 1)
    :param P: -//-
    :param D_h: -//-
    :param contains_hydrogen_sulfide:
    :param R_H_1: -//-
    :param R_H_2: -//-
    :param m2: коэффициент условий работы трубопровода
    :param gamma_m: коэффициент надежности по материалу
    :param gamma_n: коэффициент надежности по назначению трубопроводов
    :param gamma_s: коэффициент надежности по нагрузке
    :return: расчет толщины стенки трубопровода
    """
    if contains_hydrogen_sulfide:
        R = min((R_H_1 * m2) / (gamma_m * gamma_n), (R_H_2 * m2) / (0.9 * gamma_n))
    else:
        R = R_H_2 * gamma_s / gamma_n
    calculation_of_pipeline_thickness = (gamma_f * k * P * D_h) / (2 * (R + 0.6 * gamma_f * P))
    return calculation_of_pipeline_thickness


# (6.2)
# Проверка общей устойчивости подземного трубопровода в продольном направлении
def checking_stability_of_underground_pipeline_in_longitudinal_direction(S: float, m2: float, N_cp: float) -> bool:
    """
    :param S: эквивалентное продольное осевое усилие в трубопроводе, возникаю шее от действия расчетных нагрузок и
    воздействий с учетом продольных и поперечных перемещений трубопровода
    :param m2: коэффициент условий работы трубопровода
    :param N_cp: продольное критическое усилие, при котором наступает потеря про- дольной устойчивости трубопровода,
    с учетом принятого конструктивного ре шения трубопровода.
    :return: Проверка общей устойчивости подземного трубопровода в продольном направлении
    """
    return S <= m2 * N_cp


# Расчёт остаточного ресурса трубопровода по минимальной вероят ной толщине стенки труб по результатам диагностики
# ОСТ 153-39.4-010-2002 | 19 страница (7.1)
def standard_deviation_sigma(N: int, t_k: list, t_cp: float) -> float:
    """
    :param N: число участков замера
    :param t_k: результаты измерений толщин нак-х участках поверхности
    :param t_cp: средняя измеренная толщина
    :return: Среднее квадратическое отклонение
    """
    sum_of_squares = 0
    for k in range(1, N):
        sum_of_squares += (t_k[k] - t_cp) ** 2
    sigma = (sum_of_squares / (N - 1)) ** .5
    return sigma


# (7.2)
# Минимальную возможную толщину стенки с учетом пеконтролиро ванных участко в поверхности определяют для доверительной
# вероятности 95% применительно но всем промысловым трубопроводам по формуле
def minimum_possible_wall_thickness(t_cp: float, sigma: float, t_k: list, increased_accuracy: bool = False) -> float:
    """
    :param t_cp: средняя измеренная толщина
    :param sigma: Среднее квадратическое отклонение
    :return: Минимальную возможную толщину стенки
    """
    t_min = t_cp - 2 * sigma
    if increased_accuracy:
        for i in t_k:
            t_min = min(t_min, i)
    return t_min


# (7.3)
# Средняя скорость коррозии стенки трубопровода
def average_corrosion_rate_of_pipeline_wall(t_n: float, t_min: float, tau: float) -> float:
    """
    :param t_n: номинальная толщина стенки
    :param t_min: Минимальную возможную толщину стенки
    :param tau: время эксплуатации трубопровода, лет
    :return: Средняя скорость коррозии стенки трубопровода
    """
    V_cp = (t_n - t_min) / tau
    return V_cp


# (7,4)
# Остаточный ресурс трубопровода
def residual_life_of_pipeline(t_min: float, t_otb: float, V_cp: float) -> float:
    """
    :param t_min: Минимальную возможную толщину стенки
    :param t_otb: толщина стенки трубы или детали трубопровода, м, при которой они должны быть изъяты из эксплуатации
    :param V_cp: Средняя скорость коррозии стенки трубопровода
    :return:
    """
    tau_ost = (t_min - t_otb) / V_cp
    return tau_ost


# ОСТ 153-39.4-010-2002 | 20 страница (8.1)
# Вероятностный расчёт остаточного ресурса с учётом общего коррозионно-зрозненного износа стенки трубы
def internal_pressure_pipeline_element_can_withstand(t_n, delta_0, delta, R_H_1, m2, k1, alfa, D_n) -> float:
    """
    t: Текущую толщину стенки
    :param k1: -//-
    :param m2: -//-
    :param R_H_1: -//-
    :param t_n: номинальная толщина стенки
    :param delta_0: начальное технологическое изменение толщины стенки
    :param delta: износ стени
    :param alfa:-//-
    :param D_n:-//-
    :return:
    """
    t = t_n - delta_0 - delta
    R1 = R_H_1 * m1 * m2 * k1
    P_0 = (2 * t * R1) / (n * alfa * D_n)
    return P_0


# (8.2)
# P_0_n = internal_pressure_pipeline_element_can_withstand(...)
def have_pipeline_strength_during_operation(P_0_n, delta_0, delta, t_n, P) -> bool:
    """
    :param P_0_n: внутреннее давление которое может выдержать элемент трубопровода
    :param delta_0: -//-
    :param delta: -//-
    :param t_n: -//-
    :param P: рабочее давление
    :return:
    """
    delta_0_ = delta_0 / t_n
    delta_ = delta / t_n
    return P_0_n * (1 - delta_0_ - delta_) >= P


# (8.3) (8.4)
# условне прочности трубопровода в терминах относительного износа можно представить в виде
def conditional_strength_of_pipeline(t_R, t_n, delta_0, delta) -> bool:
    """
    :param t_R: расчетная толщина стенки
    :param t_n:-//-
    :param delta_0:-//-
    :param delta: текущий относительный износ стенки
    :return:
    permissible_relative_wear_of_wall: допустимый относительный износ стенки
    """
    permissible_relative_wear_of_wall = 1 - t_R / t_n - delta_0
    return permissible_relative_wear_of_wall >= delta


# 8.5
# Процесс износа стенки
def wall_wear_process(a, tau, m) -> float:
    """
    :param a: случайный параметр
    :param tau: время эксплуатации трубопровода, лет
    :param m: детерминированный параметры
    :return:Процесс износа стенки
    """
    delta = a * tau ** m
    return delta


# 8.6
# среднего относительного износа трубопровода
def average_relative_wear_of_pipeline(t_k: list, t_nk: list, N_i: int) -> float:
    """
    :param t_k: текущая толщина стенки в месте к-го замера
    :param t_nk: ноинальная толщина стенки диагностируемого элемента
    :param N_i: Число замеров толщины стенки при каждом диагностирование
    :return:
    """
    sigma = 0
    for k in range(1, N_i):
        sigma += 1 - t_k[k] - t_nk[k]
    delta_icp = 1 / N_i * sigma
    return delta_icp


# 8.7
# Статистическая оценка среднего квадратического отклонения параметра а
def statistical_estimate_of_standard_deviation_of_a(delta_cp, tau_d, t_n, t_k: list, S_0, tau_i: list, m, N) -> float:
    """
    :param N: Число замеров толщины стенки при каждом диагностирование
    :param tau_d: паработка на момент носледнего диагностирования
    :param m: детерменированный параметр
    :param delta_cp: средний относительный износ стенки в момент времени
    :param t_n: ноинальная толщина стенки
    :param t_k: текущая толщина стенки в месте к-го замера
    :param S_0: начальное среднеквадратическое отклонение толщины стенки
    :param tau_i: время диагностирования, когда проводился данный К-й замер тол пы стенки
    :return:
    """
    a_cp = delta_cp / tau_d ** m
    sigma = 0
    for i in range(1, N):
        delta_k = (t_n - t_k[k]) / t_n
        sigma += (delta_k ** 2 - S_0 ** 2) / tau_i[k] ** (2 * m) - a_cp ** 2
    S_a = (1 / (N - 1) * sigma) ** .5
    return S_a


# 8.8

def statistical_estimate_of_standard_deviation_of_a_in_moment(S_delta, S_0, tau_d, m) -> float:
    """
    :param S_delta: среднее квадратическое отклонение относительной толщины стенки в момент времени
    :param S_0: начальное среднеквадратическое отклонение толщины стенки
    :param tau_d: время диагностирования
    :param m: детерменированный параметр
    :return:
    """
    S_a = ((S_delta ** 2 - S_0 ** 2) / tau_d ** m) ** .5
    return S_a

#8.9
#Дисперсия допустимого относительного износа
#длч практики S_delta_in_square_brackets = S_0 = 0.05
def variance_of_permissible_relative_wear(S_0, S_t) -> float:
    """
    :param S_0:
    :param S_t:
    Дисперсия начального технологического отклонения и значений t_R / t_n для сентов трубопровода
    :return:
    """
    S_delta_in_square_brackets = (S_0**2 + S_t**2)**.5
    return S_delta_in_square_brackets
