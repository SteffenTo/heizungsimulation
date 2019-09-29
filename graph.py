import matplotlib.pyplot as plt
import numpy as np
def graph(waermestrom_durchschnitt, ref_waermestrom_durchschnitt,  plot_days, waermestrom_stuendlich, ref_waermestrom_stuendlich):
    plt.figure(figsize=(10, 5), num="Jahresverlauf")
    plt.plot(range(1, 13), np.absolute(waermestrom_durchschnitt), label="Gewählte Dämmung")
    plt.plot(range(1,13), np.absolute(ref_waermestrom_durchschnitt), label="Referenz ungedämmter Altbau")
    plt.legend()
    plt.title("Jahresverlauf")
    plt.xlabel("Monat")
    plt.ylabel("Durchschnittswärmestrom (in kWh)")


    plt.figure(figsize=(10, 5), num="Tagesverlauf")

    for (day, month) in plot_days:
        tageswaermestrom = waermestrom_stuendlich[
                           (day - 1) * 24 + (month - 1) * 24 * 30: day * 24 + (month - 1) * 24 * 30]
        plt.plot(np.absolute(tageswaermestrom), label=str(day) + "." + str(month))
        ref_tageswaermestrom = ref_waermestrom_stuendlich[
                               (day - 1) * 24 + (month - 1) * 24 * 30: day * 24 + (month - 1) * 24 * 30]
        plt.plot(np.absolute(ref_tageswaermestrom), label="Referenz " + str(day) + "." + str(month))

    plt.legend()
    plt.ylabel("Wärmestrom (in kWh)")
    plt.xlabel("Uhrzeit (in Stunden)")
    plt.title("Tagesverlauf")
    plt.show()
