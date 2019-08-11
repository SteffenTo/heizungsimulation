import math


def main():
    def flaechenberechnung():
        # Flächen werden für Berechnung des Wärmewiderstands benötigt
        b_haus = 8  # Initialbelegung der Variablen für die Breiten- und Höhenangaben
        l_haus = 10

        h_erdgeschoss = 3.5
        h_dach = 4.5

        h_fenster = 1.4
        b_fenster = 1.14

        h_tuer = 2.1
        b_tuer = 0.85

        b_dachfenster = 0.66
        h_dachfenster = 0.98

        tuer = h_tuer * b_tuer  # Berechnung sämtlicher Flächen
        fenster = h_fenster * b_fenster
        dachfenster = b_dachfenster * h_dachfenster

        boden = l_haus * b_haus
        wand_kurz = b_haus * (h_erdgeschoss + 0.5 * h_dach) - fenster - tuer
        wand_lang = l_haus * h_erdgeschoss - 2 * fenster
        dach = math.sqrt(h_dach ** 2 + 0.25 * b_haus ** 2) * l_haus - dachfenster

        return tuer, fenster, dachfenster, boden, wand_kurz, wand_lang, dach  # Rückgabe sämtlicher Flächen, da sie sonst nur als
        # private Variablen innerhalb der Funktion vorliegen

    flaeche_tuer, flaeche_fenster, flaeche_dachfenster, flaeche_boden, flaeche_wand_kurz, flaeche_wand_lang, flaeche_dach \
        = flaechenberechnung()



    # Berechnung der Wärmewiderstände des Hauses und des Bodens
    def waermewiderstand(lambda_glas, s_fenster, status_styropor_wand, status_styropor_boden, status_styropor_dach,
                         s_styropor, flaeche_tuer, flaeche_fenster, flaeche_dachfenster, flaeche_wand_lang,
                         flaeche_wand_kurz, flaeche_dach, flaeche_boden):

        # Deklaration der Konstanten
        s_putz = 0.025
        s_mauer = 0.115
        lambda_putz = 0.85
        lambda_hochlochziegeln = 0.95
        lambda_styropor = 0.035

        # allgemeine Funktion zur Berechnung eines einzelnen Wärmewiderstandes
        def r_lambda(s, lambda_allgemein, flaeche):
            r_lambda = s / (lambda_allgemein * flaeche)
            return r_lambda

        # Berechung des Wärmewiderstandes, der oft benötigten Kombination Putz + Ziegel + Putz + evtl. Styropor
        def r_lambda_pzs(status_styropor, s_styropor, flaeche):
            r_lambda_pzs = r_lambda(s_putz, lambda_putz, flaeche) + \
                           r_lambda(s_mauer, lambda_hochlochziegeln, flaeche)
            if not status_styropor:
                pass
            else:
                r_lambda_pzs += r_lambda(s_styropor, lambda_styropor, flaeche)
            return r_lambda_pzs

        r_lambda_dach = ((1 / r_lambda_pzs(status_styropor_dach, s_styropor, flaeche_dach)) + (
                1 / r_lambda(s_fenster, lambda_glas, flaeche_dachfenster))) ** (-1)

        r_lambda_k_wand = ((1 / r_lambda_pzs(status_styropor_wand, s_styropor, flaeche_wand_kurz)) + (
                1 / r_lambda(s_fenster, lambda_glas, flaeche_tuer)) + (
                                   1 / r_lambda(s_fenster, lambda_glas, flaeche_fenster))) ** (-1)

        r_lambda_l_wand = ((1 / r_lambda_pzs(status_styropor_wand, s_styropor, flaeche_wand_lang)) + (
                2 / r_lambda(s_fenster, lambda_glas, flaeche_fenster))) ** (-1)

        r_lambda_boden = r_lambda_pzs(status_styropor_boden, s_styropor, flaeche_boden)

        r_lambda_haus = ((2 / r_lambda_dach) + (2 / r_lambda_k_wand) + (2 / r_lambda_l_wand)) ** (-1)

        return r_lambda_haus, r_lambda_boden

    r_lambda_haus, r_lambda_boden = waermewiderstand(5.6, 0.004, False, False, False, 0.15, flaeche_tuer,
                                                     flaeche_fenster, flaeche_dachfenster, flaeche_wand_lang,
                                                     flaeche_wand_kurz, flaeche_dach, flaeche_boden)
    print(r_lambda_haus)
    print(r_lambda_boden)


main()
