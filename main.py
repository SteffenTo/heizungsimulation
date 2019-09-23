import math as m
from temperaturverlauf import get_temperaturverlauf_aussen
from temperaturverlauf import get_temperaturverlauf_keller_funktion
from waermestrom import calculate
from waermestrom import waermestrom_durchschnitt_berechnung
from waermewiderstand_flaechen import flaechenberechnung
from waermewiderstand_flaechen import waermewiderstand
from auswahl_daemmung import daemmung_wahl, soll_temperatur
from auswahl_temperatur import randbedingungen, datum_wählen
from graph import graph
import numpy as np
import matplotlib.pyplot as plt

months_start = 1
months_end = 12
days = 0  # Kann von 0-30 gehen, 0 steht für einen Start am 1. des Monats um 0 Uhr

status_styropor_wand, status_styropor_boden, status_styropor_dach, s_styropor, s_fenster, lambda_glas = daemmung_wahl()
temp_min, temp_max, temp_diff, tmin = randbedingungen()
t_tag, t_nacht, t1, t2 = soll_temperatur()
plot_days = datum_wählen()

# Aufrufen der Flächenberechnung
flaeche_tuer, flaeche_fenster, flaeche_dachfenster, flaeche_boden, flaeche_wand_kurz, flaeche_wand_lang, flaeche_dach \
    = flaechenberechnung()
# Aufrufen der Wärmewiderstandsberechnung
r_lambda_haus, r_lambda_boden = waermewiderstand(lambda_glas, s_fenster, status_styropor_wand, status_styropor_boden,
                                                 status_styropor_dach, s_styropor, flaeche_tuer,
                                                 flaeche_fenster, flaeche_dachfenster, flaeche_wand_lang,
                                                 flaeche_wand_kurz, flaeche_dach, flaeche_boden)

temperaturverlauf_aussen = get_temperaturverlauf_aussen(months_start, months_end, days, temp_diff, temp_max, temp_min, tmin)
temperaturverlauf_keller = get_temperaturverlauf_keller_funktion(months_start, months_end, days)
waermestromverlauf_waende = calculate(temperaturverlauf_aussen, r_lambda_haus, t_tag, t_nacht, t1, t2)
waermestromverlauf_boden = calculate(temperaturverlauf_keller, r_lambda_boden,  t_tag, t_nacht, t1, t2)

#waermestrom_gesamt = sum(waermestromverlauf_boden) + sum(waermestromverlauf_waende)                    #braucht man glaube ich für den Energieverbrauch
waermestrom_stuendlich = np.array(waermestromverlauf_boden) + np.array(waermestromverlauf_waende)

#Berechnen des Durchschnittlichen Waermestroms pro Monat
waermestrom_durchschnitt = waermestrom_durchschnitt_berechnung(months_start, months_end, waermestrom_stuendlich)

# print("gesamt")
# plt.plot(waermestrom_stuendlich)
# plt.show()5

# Aufrufen der Graphenerzeugung
graph(waermestrom_durchschnitt, plot_days, waermestrom_stuendlich, "Jahresvergleich", "Tagesvergleich")

#Wiederholung der Rechnung für ungedämmten Altbau
r_lambda_haus, r_lambda_boden = waermewiderstand(5.6, 0.004, False, False, False, 0, flaeche_tuer,
                                                 flaeche_fenster, flaeche_dachfenster, flaeche_wand_lang,
                                                 flaeche_wand_kurz, flaeche_dach, flaeche_boden)

waermestromverlauf_waende = calculate(temperaturverlauf_aussen, r_lambda_haus, t_tag, t_nacht, t1, t2)
waermestromverlauf_boden = calculate(temperaturverlauf_keller, r_lambda_boden, t_tag, t_nacht, t1, t2)

waermestrom_gesamt = sum(waermestromverlauf_boden) + sum(waermestromverlauf_waende)
waermestrom_stuendlich = np.array(waermestromverlauf_boden) + np.array(waermestromverlauf_waende)

#Berechnen des Durchschnittlichen Waermestroms pro Monat
waermestrom_durchschnitt = waermestrom_durchschnitt_berechnung(months_start, months_end, waermestrom_stuendlich)


# Aufrufen der Graphenerzeugung
graph(waermestrom_durchschnitt, plot_days, waermestrom_stuendlich, "Referenzjahresvergleich ungedämmter Altbau", "Referenztagesvergleich ungedämmter Altbau")
