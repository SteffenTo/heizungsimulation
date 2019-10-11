print("Ein Haus mit bekannten Abmaßen soll gedämmt werden.\n"
      "Für die Bewertung der Maßnahmen steht Ihnen eine Software zur Verfügung, welche den notwendigen Energiebbedarf\n"
      "in Kombination mit verschiedenen Dämmmaßnahmen errechnet.\n"
      "Sie können entweder die Wände,das Dach oder die Kellerdecke mit 6cm, 10cm oder 15cm dicken Styropor dämmen\n"
      "oder bei den Fenstern und Türen die Einfachverglasung durch eine Doppel- oder Dreifachverglasung ersetzen.\n"
      "Es ist ebenso möglich, das gesamte Gebäude mit 15cm Styropor und Dreifachverglasung zu dämmen\n"
      "oder den ungedämmten Altbau zu betrachten")


# 2. Verschleifung: Auswahl der möglichen Styropordicken, möglich für Wände/Dach/Boden
def s_styropor_wahl():
    if maßnahme == "a":
        s_styropor = 0.06
        return (True, True, s_styropor)  # return (allgemeinen Status, korrekte Eingabe, Styropordicke)

    elif maßnahme == "b":
        s_styropor = 0.1
        return (True, True, s_styropor)
    elif maßnahme == "c":
        s_styropor = 0.15
        return (True, True, s_styropor)
    else:  # für den Fall einer ungültigen Eingabe
        print("\nEingabe der Komponente ist ungültig. Bitte neue Komponente auswählen.\n")
        s_styropor = 0
        return (False, False, s_styropor)


# 2. Verschleifung: Auswahl der möglichen Verglasung, möglich für Fenster und Türen (immer zusammen)
def glas_wahl():
    if maßnahme == "a":
        s_fenster = 0.026
        lambda_glas = 0.012
        return (s_fenster, lambda_glas, True)  # return (Glasdicke, Wärmeleitfähigkeit, korrekte Eingabe)

    elif maßnahme == "b":
        s_fenster = 0.044
        lambda_glas = 0.004
        return (s_fenster, lambda_glas, True)

    else:  # für den Fall einer ungültigen Eingabe
        print("\nEingabe der Komponente ist ungültig. Bitte neue Komponente auswählen.\n")
        s_fenster = 0.004
        lambda_glas = 0.024
        return (s_fenster, lambda_glas, False)


def daemmung_wahl():
    global maßnahme
    korrekte_eingabe = False

    status_styropor_wand = False  # Festlegung der Werte für den ungedämmten Fall
    status_styropor_boden = False  # es müssen nur Veränderungen berücksichtigt und ergänzt werden
    status_styropor_dach = False
    s_styropor = 0
    s_fenster = 0.004
    lambda_glas = 0.024

    while korrekte_eingabe == False:  # solange diese Bedingung erfüllt ist, ist die Auswahl der Dämmung nicht
        # abgeschlossen
        # Legende: Gebäudekomponente
        print("Welche Gebäudekomponente soll gedämmt werden?\n 1 - Wände\n 2 - Dach\n 3 - Kellerboden\n "
              "4 - Fenster und Türen\n 5 - alles\n 6 - Betrachtung des ungedämmten Altbaus\n "
              "Bestätigen Sie alle Eingaben mithilfe der Enter-Taste")

        komponente = input("Komponente: ")  # Eingabe der Komponente durch Nutzer entsprechend der Legende

        # 1. Verschleifung: Wahl der zu dämmenden Komponente
        if komponente == "1":
            print("\nDämmung der Wände durch Styroporschicht der Dicke \n a - 6cm\n b - 10cm\n c - 15cm")
            maßnahme = input("Variante: ")  # Eingabe der Maßnahme durch Nutzer entsprechend der Legende,
            # springt in entsprechende 2. Schleife
            (status_styropor_wand, korrekte_eingabe, s_styropor) = s_styropor_wahl()  # hier: 2.Schleife für die Wahl
            # des Styropors

        elif komponente == "2":
            print("\nDämmung des Dachs durch Styroporschicht der Dicke \n a - 6cm\n b - 10cm\n c - 15cm")
            maßnahme = input("Variante: ")
            (status_styropor_dach, korrekte_eingabe, s_styropor) = s_styropor_wahl()

        elif komponente == "3":
            print("\nDämmung des Kellerboden durch Styroporschicht der Dicke \n a - 6cm\n b - 10cm\n c - 15cm")
            maßnahme = input("Variante: ")
            (status_styropor_boden, korrekte_eingabe, s_styropor) = s_styropor_wahl()

        elif komponente == "4":  # hier: 2.Schleife für die Wahl der Verglasung
            print("\nDämmung der Fenster und Türen durch\n a - Zweifach-Verbundglas\n b - Dreifach-Verbundglas")
            maßnahme = input("Variante: ")
            (s_fenster, lambda_glas, korrekte_eingabe) = glas_wahl()

        elif komponente == "5":  # keine 2. Schleife nötig, da alle notwendigen Informationen bekannt
            print("\nEs wird eine Dämmung sämtlicher Komponenten durch 15cm dickes Styropor und Dreifachverbundglas "
                  "vorgenommen")

            s_fenster = 0.044
            lambda_glas = 0.004
            s_styropor = 0.15
            status_styropor_boden = True
            status_styropor_wand = True
            status_styropor_dach = True
            korrekte_eingabe = True

        elif komponente == "6":  # keine 2. Schleife nötig, da alle notwendigen Informationen bereits zu Beginn bekannt
            korrekte_eingabe = True
            print("\nEs wird der Wärmestrom des ungedämmten Altbaus betrachtet")

        else:  # für den Fall einer ungültigen Eingabe
            print("\nEingabe der Komponente ist ungültig. Bitte neue Komponente auswählen.\n")
    return (status_styropor_wand, status_styropor_boden, status_styropor_dach, s_styropor, s_fenster, lambda_glas)


def check_type():
    korrekte_eingabe = False
    while korrekte_eingabe == False:
        try:
            x = int(input("Eingabe: "))
            korrekte_eingabe = True
            return x
        except ValueError:
            print("Bitte geben Sie eine Zahl ein")


def randbedingung_innen():
    korrekte_eingabe = False
    korrekt_tag = False
    korrekt_nacht = False
    korrekt_t1 = False
    korrekt_t2 = False

    while korrekte_eingabe == False:
        print("\nMöchten Sie Standardwerte für den Raumtemperaturverlauf verwenden? 'j' = ja oder 'n' = nein ?")
        s = input("Eingabe: ")
        if s.lower() == "j":
            t_tag = 21
            t_nacht = 18
            t1 = 7
            t2 = 22
            korrekte_eingabe = True

        elif s.lower() == "n":
            print("\nGeben Sie an, welche Innentemperatur tagsüber angestrebt wird."
                  "Die Wahl muss zwischen 19 und 23°C liegen.")
            while korrekt_tag == False:
                t_tag = check_type()
                if 19 <= t_tag <= 23:
                    korrekt_tag = True
                else:
                    print("Diese Temperatur ist unzulässig. Bitte tätigen Sie eine gültige Eingabe.")

            print("\nGeben Sie an, welche Innentemperatur nachts angestrebt wird."
                  "Die Wahl muss zwischen 16 und 19°C liegen.")

            while korrekt_nacht  == False:
                t_nacht = check_type()
                if 16 <= t_nacht <= 19:
                    korrekt_nacht  = True
                else:
                    print("Diese Temperatur ist unzulässig. Bitte tätigen Sie eine gültige Eingabe.")

            print("\nGeben Sie an, ab welchem Zeitpunkt, die Tagestemperatur vorliegen soll. "
                  "Dieser muss zwischen 5 und 9 Uhr morgens liegen")
            while korrekt_t1 == False:
                t1 = check_type()
                if 5 <= t1 <= 9:
                    korrekt_t1 = True
                else:
                    print("Dieser Zeitpunkt ist unzulässig. Bitte tätigen Sie eine gültige Eingabe.")

            print("\nGeben Sie an, ab welchem Zeitpunkt, die Nachttemperatur vorliegen soll. "
                  "Dieser muss zwischen 20 und 23 Uhr abends liegen")
            while korrekt_t2 == False:
                t2 = check_type()
                if 20 <= t2 <= 23:
                    korrekt_t2 = True
                else:
                    print("Dieser Zeitpunkt ist unzulässig. Bitte tätigen Sie eine gültige Eingabe.")
            korrekte_eingabe = True
        else:
            print("Bitte tätigen Sie eine gültige Eingabe.")
    return (t_tag, t_nacht, t1, t2)
