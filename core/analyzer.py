class StrompreisAnalyzer:
    
    def finde_beste_startzeit(self, preis_daten, laufzeit_stunden):
        """Findet das aufeinanderfolgende Zeitfenster mit dem niedrigsten Durchschnittspreis"""
        if not preis_daten or len(preis_daten) < laufzeit_stunden:
            return {"fehler": "Nicht genügend Preisdaten für diese Laufzeit vorhanden."}
        
        laufzeit_stunden = int(laufzeit_stunden)
        beste_zeit = None
        min_durchschnitt = float('inf')
        
        # Sliding-Window-Algorithmus, um die günstigsten aufeinanderfolgenden Stunden zu finden
        for i in range(len(preis_daten) - laufzeit_stunden + 1):
            fenster = preis_daten[i:i + laufzeit_stunden]
            summe = sum(item["preis"] for item in fenster)
            durchschnitt = round(summe / laufzeit_stunden, 2)
            
            if durchschnitt < min_durchschnitt:
                min_durchschnitt = durchschnitt
                beste_zeit = preis_daten[i]["uhrzeit"]
                
        return {
            "start_time": beste_zeit,
            "durchschnitt_preis": min_durchschnitt
        }