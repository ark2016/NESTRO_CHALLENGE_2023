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


# Расчёт остаточного ресурса трубопровода по минимальной вероятной толщине стенки труб по результатам диагностики
# ОСТ 153-39.4-010-2002 | 19 страница (7.1)
def standard_deviation_sigma(N: int, t_k: list, t_cp: float) -> float:
    """
    :param N: число участков замера
    :param t_k: результаты измерений толщин нак-х участках поверхности
    :param t_cp: средняя измеренная толщина
    :return: Среднее квадратическое отклонение
    """
    sum_of_squares = 0
    for k in range(N):
        sum_of_squares += (t_k[k] - t_cp) ** 2
    sigma = (sum_of_squares / (N - 1)) ** .5
    return sigma


# (7.2)
# Минимальную возможную толщину стенки с учетом пеконтролиро ванных участко в поверхности определяют для доверительной
# вероятности 95% применительно но всем промысловым трубопроводам по формуле
def minimum_possible_wall_thickness(t_cp: float, sigma: float, t_k: list, increased_accuracy: bool = False) -> float:
    """
    :param t_k: результаты измерений толщин нак-х участках поверхности
    :param increased_accuracy: flag
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
    for k in range(N_i):
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
    for i in range(N):
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


# 8.9
# Дисперсия допустимого относительного износа
# длч практики S_delta_in_square_brackets = S_0 = 0.05
def variance_of_permissible_relative_wear(S_0, S_t) -> float:
    """
    :param S_0:
    :param S_t:
    Дисперсия начального технологического отклонения и значений t_R / t_n для сентов трубопровода
    :return:
    """
    S_delta_in_square_brackets = (S_0 ** 2 + S_t ** 2) ** .5
    return S_delta_in_square_brackets


# ________________________________________________РД 39-0147323-339-89-Р_________________________________________________

# const

g = 9.81
e = np.e
pi = np.pi
# коэффициент кинематической вязкости воды
nu_v = 10 ** (-6)
ro_v=997 #плотность воды


# 2.8.1 c. 6 (1-2)
# условный диаметр трубопровода, обеспечивающий антикоррозионный режим течения жидкости
def nominal_pipeline_diameter(mu_h, Q_cm, nu_c, ro_c, beta, sigma, ro_b, ro_e, ro_h, nu_h) -> float:
    """
    :param mu_h: динамическая вязкость безводной дегазированной нефти, мПа'С;
    :param Q_cm:объемный секундный расход смеси, м^3/с;
    :param nu_c: коэффициент кинематической вязкости среды и нефти, соответственно, м^2/с;
    :param nu_h: коэффициент кинематической вязкости среды и нефти, соответственно, м^2/с;
    :param ro_c: плотность среды
    :param beta: расходное газоеодержание
    :param sigma: поверхностное натяжение на границе нефть вода, Н/м;
    :param ro_b: плотность воды
    :param ro_e: плотность эмульсии
    :param ro_h: плотность нефти
    :return: условный диаметр трубопровода, обеспечивающий антикоррозионный режим течения жидкости
    """
    if mu_h <= 25:
        D_kr = ((Q_cm * nu_c ** 0.0733 * ro_c ** 0.536 * (-10.96 * beta ** 2 + 9.94 * beta + 1) ** 0.659) /
                (5.254 * sigma ** 0.171 * (g * (ro_b - ro_e)) ** 0.366)) ** 0.441
    else:
        D_kr = ((Q_cm * ro_h ** 0.615 * nu_h ** 0.231) /
                (1.916 * sigma ** 0.41 * (g * (ro_b - ro_e)) ** 0.205 * e ** (2.22 * beta ** 7.63))) ** 0.494
    return D_kr


# максимальной длины ветви нефтесбора
# D_kr = nominal_pipeline_diameter(...)

# Значение максимальной длины ветви Lmax является
# расстоянием от пункта сбора до наиболее удаленного куста,
# продукция которого собирается на данный пункт. Расстановка
# пунктов сбора с лимитированной длиной ветви обеспечивает
# работу трубопроводов в антикоррозионном режиме на
# 85— 100% участков системы нефтегазосбора, то есть позволяет наиболее эффективно использовать технологические методы защиты от коррозии.
# РД 39-0147323-339-89-Р
def calculation_of_max_len_of_oil_collection_branch(delta_P, D_kr, beta, Q_cm, ro_e, lambda_cm) -> float:
    """
    :param delta_P: перепад давления на ветви, Па;
    :param D_kr: условный диаметр трубопровода
    :param beta: расходное газоеодержание
    :param Q_cm: объемный секундный расход смеси, м^3/с;
    :param ro_e: плотность эмульсии
    :param lambda_cm: коэффициент гидравлического сопротивления смеси, рассчитываемый в соответствии с ВСН 2.38 85.
    :return: расчет максимальной длины ветви нефтесбора
    """
    L_max = (delta_P * D_kr * pi ** 2 * (1 - beta)) / (8 * Q_cm ** 2 * ro_e * lambda_cm)
    return L_max


# Критическая скорость выноса рыхлых осадков водной фазой расслоенного потока
def critical_drift_speed(ro_h, ro_b, S, psi, D) -> float:
    """
    :param ro_h: плотность осадка кг/м^3
    2650
    :param ro_b: плотность воды кг/м^3
    :param S: объемная концентрация твердой фазы, м^3/м^3
    2*10**5
    :param psi: коэффициент фиктивного лобового сопротивления (табл. 1) РД 39-0147323-339-89-Р
    :param D: внутренний диаметр трубопровода, м
    10**(-3)
    :return: Критическая скорость выноса рыхлых осадков водной фазой расслоенного потока
    """
    U_kp = 710 * (nu_v * (ro_h - ro_b) / ro_b) ** (1 / 3) * (S * psi) ** (1 / 6) * D ** (1 / 3)
    return U_kp


# Если по отдельному участку нефтесбора отсутствуют данные анализа воды, допускается рассчитывать их по сред ним
# химическим составам вод различных пластов и объемам их добычи или по химическому составу вод всех скважин и их
# дебитам с использованием аддитивных зависимостей

def get_water_analysis_data_available(n, marr: list, qarr: list) -> float:
    """
    :param n:
    :param marr:значения определяемого фактора для каждого пласта;
    :param qarr: Объем воды данного пласта, поступающей в трубо провод
    :return:
    """
    MQ = 0
    Q = 0
    for i in range(n):
        MQ += marr[i] * qarr[i]
        Q += qarr[i]
    M_cp = MQ / Q
    return M_cp


# Расчет максимальной скорости коррозии
# параметры беруться из таблицы 2 РД 39-0147323-339-89-Р
def calculation_of_max_corrosion_rate(K_Cl, K_HCO3, K_Ca, K_pH, K_p, K_v_cm, K_v_cm_v_kp) -> float:
    K_x = K_Cl * K_HCO3 * K_Ca * K_pH
    K_r = K_p * K_v_cm * K_v_cm_v_kp
    ro_max = K_x * K_r
    return ro_max


# Существование антикоррозионного режима 16 c
def existence_of_anti_corrosion_regime(mu_h, n, D, beta, sigma, ro_n, ro_v, mu_np, v_n) -> bool:
    """
    :param v_n: коэффициент кинетической вязкости нефти
    :param mu_h: динамическая Вязкость безводной дегазированной нефти
    :param n: доля воды весовая
    :param D: внутренний диаметр, м
    :param beta:
    :param sigma: поверхностное натяжение на границе нефть вода
    :param ro_n: плотность нефти
    :param ro_v: плотность воды
    :param mu_np:
    :return:
    """
    if mu_h <= 25 and n < .3:
        b = beta / (1 - beta)
        if 0 < b < 2.72:
            F_r_kr = .159 / (1 - n) ** 2
        else:
            if 2.72 <= b < 7.38 or beta == 0.88:
                F_r_kr = .02 / (1 - n) ** 2 * b ** 2
            else:
                # потом добавить тесты на beta
                F_r_kr = (23 * b / (1 + b) - 19) * (1 - n) ** (-2)
        v_kr = (F_r_kr * g * D) ** 0.5
    else:
        if mu_h > 25 and n >= .3:
            ro_e = .8 * ro_n + .2 * ro_v
            if n < .5:
                v_c = mu_np / ro_e * 1.8
            else:
                v_c = v_b = 10 ** (-6)
            v_kr = (6.69 * (D ** .268 * sigma ** .171 * abs((ro_v - ro_e) * g) ** .366) /
                    (v_c ** .073 * ro_e ** .536 * abs(-10.96 * beta ** 2 + 9.94 * beta + 1) ** .659))
        else:
            v_kr = 2.44 * (sigma ** 2 * (ro_v - ro_n) * g * D ** .125 /
                           (ro_n ** 3 * v_n ** 1.125)) ** .205 * e ** (2.22 * beta ** 7.63)
    return v_kr


# Алгоритм расчета
# среднее давление на участке. Па

def average_pressure_in_area(P_n, P_k) -> float:
    P_cp = (P_n - P_k) / 2
    return P_cp


# 20 c


# Расчет параметров при прогнозировании аварий и отбраковке трубопроводов
# Для оценки возможности возникновения аварии в n-м году с начала эксплуатации рассчитывается величина
def assessing_possibility_of_accident(n, K: list, ro_max, sigma_ct) -> float:
    """
    :param n: годы эксплуатации
    :param K: коэффициент, учитывающий применение ингибиторов коррозии в 1-м году;
    в случае ингибирования К. = 0,3; без ингибирования К = 1
    :param ro_max: максимально возможная при данных физико-хими- ческих свойствах среды и гидродинамических параметрах
    движения смеси скорость коррозии, характеризующая локальные коррозионные поражения в 1-м году,
    мм/год (см. приложение 1)
    :param sigma_ct: толщина стенки трубопровода, мм
    :return:
    """
    sigma = 0
    for i in range(n):
        sigma += K[i] * ro_max
    P_n = sigma_ct - sigma
    return P_n


#______________________________________________________________________________________________________________________
#const
R_e_kr = 2320

def get_v_kr(n, d) -> float:
    """
    k: критическим числом Рейнольдса
    :param n: кинематическому коэффициенту вязкости жидкости
    :param d: диаметру трубопровода
    :return:
    """
    k = R_e_kr
    v_kr = k * n / d
    return v_kr

#зависимость критической скорости потока от основных параметров потока.

def dependence_of_critical_flow_velocity(sigma, ro_v, ro_n, mu_n, beta_b, D, beta_in, mu_v) -> float:
    """
    :param sigma: поверхностное натяжение на границе раздела между нефтью и водой, Н/м
    :param ro_v: плотность воды, кг/м;
    :param ro_n: плотность нефти, кг/м;
    :param mu_n: вязкость нефти, мПа/с;
    :param beta_b: обводненность нефти, доли ед.;
    :param D: внутренний диаметр нефтепровода, м;
    :param beta_in: обводненность в точке инверсии фаз, доли ед.
    :param mu_v: вязкость воды, мПа/с;
    :return:
    """
    w_kr = (.07 * (sigma**.56 * (g * (ro_v - ro_n))**.24) / (D**.21 * ro_n**.19 * mu_n**.61 * (1 - beta_b)**.38) *
            ((beta_in - beta_b) / beta_in)**(-0.48) * ((3 * mu_v + 3 * mu_n) / (3 * mu_v + 2 * mu_n))**.81)
    return w_kr