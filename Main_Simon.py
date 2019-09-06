"""
Created on Tue Jul 30 19:00:07 2019

@author: sbeckmann
"""
import math as m
from temperaturverlauf import get_temperaturverlauf
from waermestrom import calculate
from waermewiderstand_flaechen import flaechenberechnung
from waermewiderstand_flaechen import waermewiderstand
from auswahlmechanismus import daemmung_wahl
import numpy as np
import matplotlib.pyplot as plt


status_styropor_wand, status_styropor_boden, status_styropor_dach, s_styropor, s_fenster, lambda_glas = daemmung_wahl()

months_start = 1
months_end = 12
days = 0                                                    #Kann von 0-30 gehen, 0 steht für einen Start am 1. des Monats um 0 Uhr
korrekte_eingabe = False
while korrekte_eingabe == False:
    s = input("Wollen Sie Standardwerte verwenden? 'j' oder 'n' ?")
    if s.lower() == "j":
        temp_min = 1
        temp_max = 20
        temp_diff = 4
        tmin = 2
        r_waende = 5
        r_boden = 3
        korrekte_eingabe = True
        
        #23nraw_days =  ["1.1", "1.4.", "1.7", "1.10"]
              
    elif s.lower() == "n":
        temp_min = float(input("Geben Sie die Mindesttemperatur für den 1. Januar ein: " )) 
        print (temp_min, "°C")
        temp_max = float(input("Geben Sie die Maximaltemperatur für den 1. Juli ein: " ))
        print (temp_max, "°C")
        temp_diff = float(input("Wählen Sie den Wert für den Temperaturunterschied am Tag zwischen Tagestiefst-/Tageshöchsttemperatur und der durchschnittlichen Temperatur pro Tag ein: " ))
        print (temp_diff, "°C")
        tmin = float(input("Geben Sie den Zeitpunkt der Tagestiefsttemperatur an: " ))
        print (tmin, "Uhr")
        korrekte_eingabe = True
        #print ("Für welchen Zeitraum soll die Temperatur ausgegeben werden? \n 1 - 1 Jahr\n 2 - 1. Januar\n 3 - 1. April\n 4 - 1. Juli\n 5 - 1. Oktober")
        #Auswahl = input ("Auswahl: ")
        
        #if Auswahl == "1":
        #    months_start = 1; months_end = 12; days = 0                 #Monate: 1 = Januar; Tage: 1 = 1. des Monats mit drin
        #if Auswahl == "2":
        #    months_start = 1; months_end = 1; days = 1
        #if Auswahl == "3":
        #    months_start = 4; months_end = 4; days = 1
        #if Auswahl == "4":
        #    months_start = 7; months_end = 7; days = 1
        #if Auswahl == "5":
        #   months_start = 10; months_end = 10; days = 1
    else:
        print("Bitte geben Sie eine gültige Eingabe an.")
        korrekte_eingabe = False
   

#technical conversion from list of strings to list of tuples(int, int)
    
raw_days = list()

anzahl_tage = int(input("Wie viele Tage sollen im Tagesvergleich verglichen werden? \n"))
for index in range(anzahl_tage):
    raw_days.append(input("Bitte geben sie die zu vergleichenden Tage im Format 'dd.mm' ein \n"))
    
plot_days = list()
for day in raw_days:
    plot_days.append((int(day.split(".")[0]), int(day.split(".")[1])))
# Aufrufen der Flächenberechnung
flaeche_tuer, flaeche_fenster, flaeche_dachfenster, flaeche_boden, flaeche_wand_kurz, flaeche_wand_lang, flaeche_dach \
    = flaechenberechnung()
# Aufrufen der Wärmewiderstandsberechnung
r_lambda_haus, r_lambda_boden = waermewiderstand(lambda_glas, s_fenster, status_styropor_wand, status_styropor_boden, status_styropor_dach, s_styropor, flaeche_tuer,
                                                 flaeche_fenster, flaeche_dachfenster, flaeche_wand_lang,
                                                 flaeche_wand_kurz, flaeche_dach, flaeche_boden)

temperaturverlauf_aussen = get_temperaturverlauf(months_start, months_end, days, temp_diff, temp_max, temp_min, tmin)
temperaturverlauf_keller = 
waermestromverlauf_waende = calculate(temperaturverlauf_aussen, r_lambda_haus)
waermestromverlauf_boden = calculate(temperaturverlauf_keller, r_lambda_boden)

waermestrom_gesamt = sum(waermestromverlauf_boden) + sum(waermestromverlauf_waende)
waermestrom_stuendlich = np.array(waermestromverlauf_boden) + np.array(waermestromverlauf_waende)

avg_values_per_month = list()
for month in range(months_end - months_start +1):
    #print("Monat: {}".format(month))
    waermestromverlauf_this_month = waermestrom_stuendlich[month * (24*30) : (month +1) * 24 * 30]
    avg_values_per_month.append(np.mean(waermestromverlauf_this_month))
    #plt.plot(waermestromverlauf_this_month)
    #plt.show()
    
#print("gesamt")
#plt.plot(waermestrom_stuendlich)
#plt.show()

plt.figure(figsize=(10,5))
plt.plot(range(1,13),avg_values_per_month)
plt.title("Jahresverlauf")
plt.xlabel("Monat")
plt.ylabel("Durchschnittswärmestrom (in W(h))")
plt.show()

    
plt.figure(figsize=(10,5))  

for (day, month) in plot_days:
    tageswaermestrom = waermestrom_stuendlich[(day-1) * 24+ (month - 1) * 24 * 30 : day * 24 + (month -1)* 24*30]
    plt.plot(tageswaermestrom, label = str(day) + "." + str(month))
plt.legend()
plt.ylabel('Wärmestrom (in W(h))')
plt.xlabel("Uhrzeit (in Stunden)")
plt.title("Tagesvergleiche")
plt.show()
