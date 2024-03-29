# folgende Befehle müssen nur eingebunden werden, da es sonst zu einem PyInstaller Fehler kommt
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy
# Aufrufe, die für das eigentliche Programm nötig sind
import math as m
import numpy as np
import matplotlib.pyplot as plt
from temperaturverlauf import get_temperaturverlauf_aussen, get_temperaturverlauf_keller_funktion
from temperaturverlauf import temperaturverlauf_soll, temperaturverlauf_ist
from waermestrom import berechnung, waermestrom_durchschnitt_berechnung, waermestromformel
from waermewiderstand_flaechen import flaechenberechnung, waermewiderstand
from auswahl_daemmung import daemmung_wahl
from auswahl_temperatur import randbedingung_aussen, randbedingung_innen, datum_wählen
from graph import graph

# Variablendeklaration
months_start = 1
months_end = 12
days = 0  # Kann von 0-30 gehen, 0 steht für einen Start am 1. des Monats um 0 Uhr

# Aufrufen der Daten aus der Benutzereingabe
status_styropor_wand, status_styropor_boden, status_styropor_dach, s_styropor, s_fenster, lambda_glas = daemmung_wahl()
temp_min, temp_max, temp_diff, tmin = randbedingung_aussen()
t_tag, t_nacht, t1, t2 = randbedingung_innen()
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
temperatur_soll = temperaturverlauf_soll(t1, t2, t_tag, t_nacht)
temperatur_ist = temperaturverlauf_ist(t1, t2, t_tag, t_nacht)

# Aufrufen der Wärmestromverläufe
waermestromverlauf_waende = berechnung(temperaturverlauf_aussen, r_lambda_haus, temperatur_ist)
waermestromverlauf_boden = berechnung(temperaturverlauf_keller, r_lambda_boden, temperatur_ist)

# Berechnung Gesamtenergieverbrauch
waermestrom_gesamt = sum(waermestromverlauf_boden) + sum(waermestromverlauf_waende)
# Berechnung des Wärmestroms pro Stunde
waermestrom_stuendlich = np.array(waermestromverlauf_boden) + np.array(waermestromverlauf_waende)

# Berechnen des Durchschnittlichen Waermestroms pro Monat
waermestrom_durchschnitt = waermestrom_durchschnitt_berechnung(months_start, months_end, waermestrom_stuendlich)


# Wiederholung der Rechnung für den ungedämmten Altbau
ref_r_lambda_haus, ref_r_lambda_boden = waermewiderstand(0.024, 0.004, False, False, False, 0, flaeche_tuer,
                                                 flaeche_fenster, flaeche_dachfenster, flaeche_wand_lang,
                                                 flaeche_wand_kurz, flaeche_dach, flaeche_boden)

ref_waermestromverlauf_waende = berechnung(temperaturverlauf_aussen, ref_r_lambda_haus, temperatur_ist)
ref_waermestromverlauf_boden = berechnung(temperaturverlauf_keller, ref_r_lambda_boden, temperatur_ist)

ref_waermestrom_gesamt = sum(ref_waermestromverlauf_boden) + sum(ref_waermestromverlauf_waende)
ref_waermestrom_stuendlich = np.array(ref_waermestromverlauf_boden) + np.array(ref_waermestromverlauf_waende)

ref_waermestrom_durchschnitt = waermestrom_durchschnitt_berechnung(months_start, months_end, ref_waermestrom_stuendlich)

# Benutzerausgabe
energiebedarf_daemmung = round(abs(waermestrom_gesamt), 2)
energiebedarf_referenz = round(abs(ref_waermestrom_gesamt), 2)
energieeinsparung = energiebedarf_referenz - energiebedarf_daemmung
print("\n\nDer Jahresenergiebedarf der gewählten Dämmung beträgt", energiebedarf_daemmung, "kWh.")
print("Der Referenzjahresenergiebedarf für den ungedämmten Altbau beträgt", energiebedarf_referenz, "kWh.")
print("Mit der gewählten Dämmung sparen sie", round(energieeinsparung, 2), "kWh pro Jahr. Das entspricht", round(100 -
      (energiebedarf_daemmung/energiebedarf_referenz)*100, 2), "%.")
if abs(min(ref_waermestrom_stuendlich)) < 23:
    print("Die Heizung ist für die gewählten Werte ausreichend dimensioniert.")
else:
    print("\nACHTUNG, der maximal benötigte Wärmestrom von", round(abs(min(ref_waermestrom_stuendlich)), 2),
          "kW übersteigt die maximal von der Heizung bereitstellbare Leistung von 23 kW.")
print("\n© Natalia Mrozek, Luca Podrasa, Simon Beckmann, Steffen Tomasik")

# Aufrufen der Graphenerzeugung
graph(waermestrom_durchschnitt, ref_waermestrom_durchschnitt,  daten_drucken, daten_original, waermestrom_stuendlich,
      ref_waermestrom_stuendlich, temperaturverlauf_aussen, temperatur_soll, temperatur_ist)

