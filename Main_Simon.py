# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 19:00:07 2019

@author: sbeckmann
"""
import math as m
from temperaturverlauf import get_temperaturverlauf
from waermestrom import calculate
import numpy as np
import matplotlib.pyplot as plt

months_start = 1
months_end = 12
days = 0  
s = input("Wollen Sie Standardwerte verwenden? 'j' oder 'n' ?")
if s.lower() == "j":
    temp_min = 1
    temp_max = 20
    temp_diff = 4
    tmin = 2
    r_waende = 5
    r_boden = 3
    
    #23nraw_days =  ["1.1", "1.4.", "1.7", "1.10"]
          
else:
    temp_min = float(input("Geben Sie die Mindesttemperatur für den 1. Januar ein: " )) 
    print (temp_min, "°C")
    temp_max = float(input("Geben Sie die Maximaltemperatur für den 1. Juli ein: " ))
    print (temp_max, "°C")
    temp_diff = float(input("Wählen Sie den Wert für den Temperaturunterschied am Tag zwischen Tagestiefst-/Tageshöchsttemperatur und der durchschnittlichen Temperatur pro Tag ein: " ))
    print (temp_diff, "°C")
    tmin = float(input("Geben Sie den Zeitpunkt der Tagestiefsttemperatur an: " ))
    print (tmin, "Uhr")

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
   

#technical conversion from list of strings to list of tuples(int, int)
    
raw_days = list()

anzahl_tage = int(input("Wie viele Tage sollen im Tagesvergleich verglichen werden? \n"))
for index in range(anzahl_tage):
    raw_days.append(input("Bitte geben sie die zu vergleichenden Tage im Format 'dd.mm' ein \n"))
    
plot_days = list()
for day in raw_days:
    plot_days.append((int(day.split(".")[0]), int(day.split(".")[1])))
 
     
temperaturverlauf = get_temperaturverlauf(months_start, months_end, days, temp_diff, temp_max, temp_min, tmin)
waermestromverlauf_waende = calculate(temperaturverlauf, r_waende)
waermestromverlauf_boden = calculate(temperaturverlauf, r_boden)

waermestrom_gesamt = sum( waermestromverlauf_boden) + sum(waermestromverlauf_waende)
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