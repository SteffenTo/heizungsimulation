import matplotlib.pyplot as plt
import numpy as np
def graph(avg_values_per_month, plot_days, waermestrom_stuendlich):
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, 13), np.absolute(avg_values_per_month))
    plt.title("Jahresverlauf")
    plt.xlabel("Monat")
    plt.ylabel("Durchschnittswärmestrom (in W(h))")


    plt.figure(figsize=(10, 5))

    for (day, month) in plot_days:
        tageswaermestrom = waermestrom_stuendlich[
                           (day - 1) * 24 + (month - 1) * 24 * 30: day * 24 + (month - 1) * 24 * 30]
        plt.plot(np.absolute(tageswaermestrom), label=str(day) + "." + str(month))
    plt.legend()
    plt.ylabel('Wärmestrom (in W(h))')
    plt.xlabel("Uhrzeit (in Stunden)")
    plt.title("Tagesvergleiche")
    plt.show()

