# ⚡ Strompreis-Assistent

Ein intelligenter Assistent zur Analyse von Strompreisschwankungen und zur Optimierung der Startzeiten von Haushaltsgeräten. Diese Anwendung hilft Endverbrauchern, von dynamischen Stromtarifen zu profitieren und ihre Energiekosten spürbar zu senken.

---

## 🚀 Über das Projekt

Der **Strompreis-Assistent** verbindet sich über eine API mit der Strombörse, speichert die stündlichen Marktdaten in einer lokalen Datenbank und berechnet mithilfe eines effizienten Algorithmus die kostengünstigste Laufzeit für verschiedene Haushaltsgeräte. Die Benutzeroberfläche wurde komplett mit **Streamlit** realisiert, um eine einfache und intuitive Bedienung zu ermöglichen.

### 🧠 Kernfunktionen
* **Live-Datenabruf:** Direkte Anbindung an die offizielle **aWATTar-API** zur Abfrage aktueller Börsenstrompreise.
* **Intelligente Berechnung:** Nutzen des **Sliding-Window-Algorithmus**, um das günstigste aufeinanderfolgende Zeitfenster für eine frei wählbare Gerätelaufzeit zu ermitteln.
* **Persistente Speicherung:** Lokale Datenverwaltung mit **SQLite** zur Archivierung von Marktpreisen und zur Protokollierung durchgeführter Geräte-Berechnungen (Historie).
* **Dynamisches UI:** Interaktive Dropdown-Menüs und Dashboard-Metriken zur übersichtlichen Darstellung der besten Startzeit und der geschätzten Gesamtkosten in Euro.

---

## 🛠️ Technologie-Stack

* **Programmiersprache:** Python
* **Frontend / GUI:** Streamlit
* **Datenbank:** SQLite (sqlite3)
* **API-Kommunikation:** Requests-Bibliothek
* **Datenverarbeitung:** Datetime (Konvertierung von Unix-Timestamps in lokale Uhrzeiten)

---

## 📁 Projektstruktur

```text
Strompreis-Assistent/
│
├── core/
│   ├── api_client.py     # Schnittstelle zur aWATTar-API (Datenabruf & Umrechnung)
│   ├── database.py       # Verwaltung der SQLite-Tabellen und Datenpersistenz
│   └── analyzer.py       # Mathematische Logik (Sliding-Window-Algorithmus)
│
├── main.py               # Haupteinstiegspunkt und Steuerung der Streamlit-GUI
├── .gitignore            # Ausschluss von Cache-Dateien und der lokalen daten.db
└── README.md             # Projektdokumentation
