import matplotlib.pyplot as plt
import numpy as np

def graph(waermestrom_durchschnitt, ref_waermestrom_durchschnitt,  plot_days, raw_days, waermestrom_stuendlich, ref_waermestrom_stuendlich, temperaturverlauf_aussen):
    # Jahresverbrauch
    plt.figure(figsize=(10, 5), num="Jahresverlauf")
    plt.plot(range(1,13), np.absolute(waermestrom_durchschnitt), label="Gewählte Dämmung")
    plt.plot(range(1,13), np.absolute(ref_waermestrom_durchschnitt), label="Referenz ungedämmter Altbau")
    plt.legend()
    plt.title("Jahresverlauf")
    plt.xlabel("Monat")
    plt.ylabel("Durchschnittsenergieverbrauch in kWh")


    # Tagesverlauf
    plt.figure(figsize=(10, 5), num="Tagesverlauf")

    for (day, month) in plot_days:
        tageswaermestrom = waermestrom_stuendlich[
                           (day - 1) * 24 + (month - 1) * 24 * 30: (day * 24 + (month - 1) * 24 * 30)+1]
        plt.plot(np.absolute(tageswaermestrom), label=str(day) + "." + str(month))
        ref_tageswaermestrom = ref_waermestrom_stuendlich[
                               (day - 1) * 24 + (month - 1) * 24 * 30: (day * 24 + (month - 1) * 24 * 30)+1]
        plt.plot(np.absolute(ref_tageswaermestrom), label="Referenz " + str(day) + "." + str(month))

    plt.legend()
    plt.title("Tagesverlauf")
    plt.ylabel("Energieverbrauch in kWh")
    plt.xlabel("Uhrzeit (in Stunden)")


    # Temperaturverlauf
    zaehler = 0
    for i in raw_days:
        plt.figure(figsize=(10, 5), num = str(i))
        day, month = plot_days[zaehler]
        zaehler += 1
        tagestemperaturverlauf = temperaturverlauf_aussen[
                                 (day - 1) * 24 + (month - 1) * 24 * 30: (day * 24 + (month - 1) * 24 * 30)+1]
        plt.plot(tagestemperaturverlauf, label = "Außentemperatur")

        plt.legend()
        plt.title("Temperaturverlauf für den "+ str(i))
        plt.ylabel("Temperatur in °C")
        plt.xlabel("Uhrzeit in Stunden")






    plt.show()
