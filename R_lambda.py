#Berechnung des Wärmewiderstandes mithilfe von Klasse funktioniert noch nicht
class Wärmewiderstand:
    dach = 60.208                                                       #test variablen für Variablen die von der Flächenfkt. ausgegeben werden
    dachfenster = 0.647
    fenster = 1.596
    tuer = 1.793
    k_wand = 46
    l_wand = 35
    boden = 80
    

    s_putz = 0.035                                                  #Deklaration der Attribute die für alle Beispiele der class gelten
    s_mauer = 0.115
    s_tuer = s_putz + s_mauer
    lambda_putz = 0.85
    lambda_hochlochziegeln = 0.95                 #muss evtl noch geändert werden
    lambda_styropor = 0.035

    def __init__(self, lambda_glas, s_fenster, status_styropor_wand, status_styropor_boden, status_styropor_dach, s_styropor):              #s_fenster evtl == s_wand
        self.lambda_glas = lambda_glas
        self.s_fenster = s_fenster
        self.status_styropor_wand = status_styropor_wand
        self.status_styropor_boden = status_styropor_boden
        self.status_styropor_dach = status_styropor_dach
        self.s_styropor = s_styropor

    def r_lambda(self, s, lambda_allgemein, flaeche):                              #allgemeine Funktion zur Berechnung eines einzelnen Wärmewiderstandes
        r_lambda = s/(lambda_allgemein * flaeche)
        return r_lambda
    
    def r_lambda_pzs(self, status_styropor, s_styropor, flaeche):                 #Berechung des Wärmewiderstandes von der oft benötigten Kombination Putz + Ziegel + Putz + evtl. Styropor
        r_lambda_pzs = r_lambda(s_putz, lambda_putz,flaeche) + r_lambda(s_mauer, lambda_hochlochziegeln, flaeche)
        if status_styropor == False:
            pass
        else:
            r_lambda_pzs += r_lambda(s_styropor, lambda_styropor, flaeche)
        return r_lambda_pzs
    
    r_lambda_dach = ((1/r_lambda_pzs(status_styropor_dach, s_styropor, dach)) + (1/r_lambda(s_fenster, lambda_glas, dachfenster)))**(-1)
    r_lambda_k_wand =((1/r_lambda_pzs(status_styropor_wand, s_styropor, k_wand)) + (1/r_lambda(s_tuer, lambda_glas, tuer)) + (1/r_lambda(s_fenster, lambda_glas, fenster)))**(-1)       #lambda_glas der Tür muss immer gleich bleiben und verändert sich nicht mit der Doppelverglasung
    r_lambda_l_wand = ((1/r_lambda_pzs(status_styropor_wand, s_styropor, l_wand)) + (2/r_lambda(s_fenster, lambda_glas, fenster)))**(-1)
    r_lambda_boden = r_lambda_pzs(status_styropor_boden, s_styropor, flaeche)
    
    def r_lambda_gesamt(self, lambda_glas, s_fenster, s_styropor):
        r_lambda_gesamt =((2/r_lambda_dach) + (2/r_lambda_k_wand) + (2/r_lambda_l_wand) + (1/r_lambda_boden))**(-1)
        return r_lambda_gesamt
    print("Der Wärmewiderstand des Hauses beträgt", r_lambda_gesamt(lambda_glas, s_fenster, s_styropor), "K/W.")


r_lambda_haus = Wärmewiderstand(1.2, 0.15, True, True, True, 0.15)
r_lambda_haus.r_lambda_gesamt()

        
           
