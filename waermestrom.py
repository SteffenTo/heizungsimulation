import numpy as np


def waermestromformel(temp_outside, temp_inside, r_lambda):
    if temp_outside >= temp_inside:
        return 0
    return np.divide(temp_outside - temp_inside, r_lambda)


def calculate(list_of_temperatures_outside, r_lambda, t_tag, t_nacht, t1, t2):
    waermestrom = list()

    for index, item in enumerate(list_of_temperatures_outside):
        hour = index % 24

        if t1 <= hour < t2:
            temp_inside = t_tag
        else:
            temp_inside = t_nacht

        waermestrom.append(waermestromformel(item, temp_inside, r_lambda))
    return waermestrom

        waermestrom.append(waermestromformel(item, temp_inside, r_lambda))
    return waermestrom

def waermestrom_durchschnitt_berechnung(months_start, months_end, waermestrom_stuendlich):
    waermestrom_durchschnitt = list()
    for month in range(months_end - months_start + 1):
        # print("Monat: {}".format(month))
        waermestromverlauf_this_month = waermestrom_stuendlich[month * (24 * 30): (month + 1) * 24 * 30]
        waermestrom_durchschnitt.append(np.mean(waermestromverlauf_this_month))
        # plt.plot(waermestromverlauf_this_month)
        # plt.show()
    return waermestrom_durchschnitt


