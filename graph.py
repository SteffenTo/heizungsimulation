import matplotlib.pyplot as plt
import numpy as np

def graph(waermestrom_durchschnitt, ref_waermestrom_durchschnitt,  daten_drucken, daten_original, waermestrom_stuendlich,
          ref_waermestrom_stuendlich, temperaturverlauf_aussen, temperatur_soll, temperatur_ist):

    # Temperaturverlauf
    zaehler = 0
    for i in daten_original:
        plt.figure(figsize=(10, 5), num = str(i))
        plt.grid()
        plt.xticks(np.arange(0, 25, 1.0))
        plt.xlim(0, 24)
        plt.title("Temperaturverlauf für den " + str(i))
        plt.ylabel("Temperatur in °C")
        plt.xlabel("Uhrzeit in Stunden")
        day, month = daten_drucken[zaehler]
        zaehler += 1
        tagestemperaturverlauf = temperaturverlauf_aussen[
                                 (day - 1) * 24 + (month - 1) * 24 * 30: (day * 24 + (month - 1) * 24 * 30)+1]
        plt.plot(range(0, 25), tagestemperaturverlauf, label = "Außentemperatur")
        plt.plot(np.arange(0, 25, 0.25), temperatur_soll, label = "Sollinnentemperatur")
        plt.plot(np.arange(0, 25, 0.25), temperatur_ist, label = "Istinnentemperatur")
        plt.legend()

    # Tagesverlauf
    plt.figure(figsize=(10, 5), num="Tagesverlauf")
    plt.grid()
    plt.xticks(np.arange(0, 25, 1.0))
    plt.xlim(0, 24)
    plt.title("Tagesverlauf")
    plt.ylabel("Energieverbrauch in kWh")
    plt.xlabel("Uhrzeit (in Stunden)")
    for (day, month) in daten_drucken:
        tageswaermestrom = waermestrom_stuendlich[
                           (day - 1) * 24 + (month - 1) * 24 * 30: (day * 24 + (month - 1) * 24 * 30) + 1]
        plt.plot(range(0, 25), np.absolute(tageswaermestrom), label=str(day) + "." + str(month))
        ref_tageswaermestrom = ref_waermestrom_stuendlich[
                               (day - 1) * 24 + (month - 1) * 24 * 30: (day * 24 + (month - 1) * 24 * 30) + 1]
        plt.plot(range(0, 25), np.absolute(ref_tageswaermestrom), label="Referenz " + str(day) + "." + str(month),
                 linestyle='dotted')
    plt.legend()

    # Jahresverbrauch
    plt.figure(figsize=(10, 5), num="Jahresverlauf")
    plt.grid()
    plt.xticks(np.arange(1, 13, 1.0))
    plt.xlim(1, 12)
    plt.title("Jahresverlauf")
    plt.xlabel("Monat")
    plt.ylabel("Durchschnittsenergieverbrauch in kWh")
    plt.plot(range(1, 13), np.absolute(waermestrom_durchschnitt), label="Gewählte Dämmung")
    plt.plot(range(1, 13), np.absolute(ref_waermestrom_durchschnitt), label="Referenz ungedämmter Altbau", linestyle = 'dotted')
    plt.legend()

    plt.show()
