import numpy as np


def waermestromformel(temp_aussen, temp_innen, r_lambda):
    if temp_aussen >= temp_innen:
        return 0
    return (np.divide(temp_aussen - temp_innen, r_lambda))/1000

def berechnung(liste_aussentemperaturen, r_lambda, temperatur_ist):
    waermestrom = list()

    for index, item in enumerate(liste_aussentemperaturen):
        hour = index % 24
        waermestrom.append(waermestromformel(item, temperatur_ist[hour], r_lambda))
    return waermestrom

def waermestrom_durchschnitt_berechnung(months_start, months_end, waermestrom_stuendlich):
    waermestrom_durchschnitt = list()
    for month in range(months_end - months_start + 1):
        waermestromverlauf_this_month = waermestrom_stuendlich[month * (24 * 30): (month + 1) * 24 * 30]
        waermestrom_durchschnitt.append(np.mean(waermestromverlauf_this_month))
    return waermestrom_durchschnitt


