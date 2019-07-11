class Waermewiderstand:

    def __init__(self, lambda_glas, s_fenster, status_styropor_wand, status_styropor_boden, status_styropor_dach, s_styropor):
        self.lambda_glas = lambda_glas
        self.s_fenster = s_fenster
        self.status_styropor_wand = status_styropor_wand
        self.status_styropor_boden = status_styropor_boden
        self.status_styropor_dach = status_styropor_dach
        self.s_styropor = s_styropor

        self.dach = 60.208                                          # test variablen für Variablen die von der Flächenfkt. ausgegeben werden
        self.dachfenster = 0.647
        self.fenster = 1.596
        self.tuer = 1.793
        self.k_wand = 46
        self.l_wand = 35
        self.boden = 80

        self.s_putz = 0.025                                         # Deklaration der Attribute die für Instanzen der class gelten
        self.s_mauer = 0.115
        self.s_tuer = 0.06
        self.lambda_glas_tuer = 5.6
        self.lambda_putz = 0.85
        self.lambda_hochlochziegeln = 0.95
        self.lambda_styropor = 0.035

        self.r_lambda_dach = ((1 / self.r_lambda_pzs(status_styropor_dach, s_styropor, self.dach)) + (1 / self.r_lambda(s_fenster, lambda_glas, self.dachfenster))) ** (-1)
        
        self.r_lambda_k_wand = ((1 / self.r_lambda_pzs(status_styropor_wand, s_styropor,self. k_wand)) + (1 / self.r_lambda(self.s_tuer, lambda_glas, self.tuer)) + (
                    1 / self.r_lambda(s_fenster, lambda_glas, self.fenster))) ** (-1)                                  # lambda_glas der Tür muss immer gleich bleiben und verändert sich nicht mit der Doppelverglasung

        self.r_lambda_l_wand = ((1 / self.r_lambda_pzs(status_styropor_wand, s_styropor, self.l_wand)) + (
                    2 / self.r_lambda(s_fenster, lambda_glas, self.fenster))) ** (-1)

        #self.r_lambda_boden = self.r_lambda_pzs(status_styropor_boden, s_styropor, self.boden)


    def r_lambda(self, s, lambda_allgemein, flaeche):                                                                   # allgemeine Funktion zur Berechnung eines einzelnen Wärmewiderstandes
        r_lambda = s / (lambda_allgemein * flaeche)
        return r_lambda

    def r_lambda_pzs(self, status_styropor, s_styropor, flaeche):                                                       # Berechung des Wärmewiderstandes von der oft benötigten Kombination Putz + Ziegel + Putz + evtl. Styropor
        r_lambda_pzs = self.r_lambda(self.s_putz, self.lambda_putz, flaeche) + self.r_lambda(self.s_mauer, self.lambda_hochlochziegeln, flaeche)
        if status_styropor == False:
            pass
        else:
            r_lambda_pzs += self.r_lambda(s_styropor, self.lambda_styropor, flaeche)
        return r_lambda_pzs

    def r_lambda_gesamt(self, lambda_glas, s_fenster, s_styropor):
        r_lambda_gesamt = ((2 / self.r_lambda_dach) + (2 / self.r_lambda_k_wand) + (2 / self.r_lambda_l_wand)) ** (-1)
        return r_lambda_gesamt
    
    def r_lambda_boden(self, status_styropor_boden, s_styropor, boden):
        r_lambda_boden = self.r_lambda_pzs(status_styropor_boden, s_styropor, self.boden)
        return r_lambda_boden


r_lambda_haus = Waermewiderstand(5.6, 0.004, False, False, False, 0.15)
r_lambda_haus_ohne_boden = r_lambda_haus.r_lambda_gesamt(5.6, 0.004, 0.15)
print(r_lambda_haus_ohne_boden)
r_lambda_boden = r_lambda_haus.r_lambda_boden(False, 0.15, 80)
print(r_lambda_boden)







