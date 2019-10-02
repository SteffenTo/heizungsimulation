import math as m
from temperaturverlauf import get_temperaturverlauf_aussen
from temperaturverlauf import get_temperaturverlauf_keller_funktion
from waermestrom import berechnung
from waermestrom import waermestrom_durchschnitt_berechnung
from waermestrom import waermestromformel
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
daten_drucken, daten_original = datum_wählen()

# Aufrufen der Flächenberechnung
flaeche_tuer, flaeche_fenster, flaeche_dachfenster, flaeche_boden, flaeche_wand_kurz, flaeche_wand_lang, flaeche_dach \
    = flaechenberechnung()
# Aufrufen der Wärmewiderstandsberechnung
r_lambda_haus, r_lambda_boden = waermewiderstand(lambda_glas, s_fenster, status_styropor_wand, status_styropor_boden,
                                                 status_styropor_dach, s_styropor, flaeche_tuer,
                                                 flaeche_fenster, flaeche_dachfenster, flaeche_wand_lang,
                                                 flaeche_wand_kurz, flaeche_dach, flaeche_boden)
# Aufrufen der Temperaturverläufe
temperaturverlauf_aussen = get_temperaturverlauf_aussen(months_start, months_end, days, temp_diff, temp_max, temp_min, tmin)
temperaturverlauf_keller = get_temperaturverlauf_keller_funktion(months_start, months_end, days)

# Aufrufen der Wärmestromverläufe
waermestromverlauf_waende = berechnung(temperaturverlauf_aussen, r_lambda_haus, t_tag, t_nacht, t1, t2)
waermestromverlauf_boden = berechnung(temperaturverlauf_keller, r_lambda_boden,  t_tag, t_nacht, t1, t2)

# Berechnung Gesamtenergieverbrauch
waermestrom_gesamt = sum(waermestromverlauf_boden) + sum(waermestromverlauf_waende)
# Berechnung des Wärmestroms pro Stunde
waermestrom_stuendlich = np.array(waermestromverlauf_boden) + np.array(waermestromverlauf_waende)

#Berechnen des Durchschnittlichen Waermestroms pro Monat
waermestrom_durchschnitt = waermestrom_durchschnitt_berechnung(months_start, months_end, waermestrom_stuendlich)


#Wiederholung der Rechnung für ungedämmten Altbau
ref_r_lambda_haus, ref_r_lambda_boden = waermewiderstand(0.024, 0.004, False, False, False, 0, flaeche_tuer,
                                                 flaeche_fenster, flaeche_dachfenster, flaeche_wand_lang,
                                                 flaeche_wand_kurz, flaeche_dach, flaeche_boden)

ref_waermestromverlauf_waende = berechnung(temperaturverlauf_aussen, ref_r_lambda_haus, t_tag, t_nacht, t1, t2)
ref_waermestromverlauf_boden = berechnung(temperaturverlauf_keller, ref_r_lambda_boden, t_tag, t_nacht, t1, t2)

ref_waermestrom_gesamt = sum(ref_waermestromverlauf_boden) + sum(ref_waermestromverlauf_waende)
ref_waermestrom_stuendlich = np.array(ref_waermestromverlauf_boden) + np.array(ref_waermestromverlauf_waende)

ref_waermestrom_durchschnitt = waermestrom_durchschnitt_berechnung(months_start, months_end, ref_waermestrom_stuendlich)

print("Der Jahresenergiebedarf der gewählten Dämmung beträgt", round(abs(waermestrom_gesamt), 2), "kWh.")
print("Der Referenzjahresenergiebedarf für den ungedämmten Altbau beträgt", round(abs(ref_waermestrom_gesamt), 2), "kWh.")
print("Der maximal benötigte Wärmestrom beträgt", round(abs(min(ref_waermestrom_stuendlich)), 2), "kWh.")
if abs(min(ref_waermestrom_stuendlich)) < 23:
    pass
else:
    print("Achtung, der benötigte Wärmestrom übersteigt die maximal von der Heizung bereitstellbare Leistung.")

# Aufrufen der Graphenerzeugung
graph(waermestrom_durchschnitt, ref_waermestrom_durchschnitt,  daten_drucken, daten_original, waermestrom_stuendlich, ref_waermestrom_stuendlich, temperaturverlauf_aussen)

