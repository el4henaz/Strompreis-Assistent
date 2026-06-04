import streamlit as st
# ایمپورت مستقیم بر اساس پوشه‌های موجود در پروژه 
from core.api_client import AwattarApiClient
from core.database import DatabaseManager
from core.analyzer import StrompreisAnalyzer

def main():
    # 1. Objekte der Kern-Logik erstellen
    api_client = AwattarApiClient()
    db_manager = DatabaseManager()
    analyzer = StrompreisAnalyzer()

    # 2. UI-Layout (Frontend)
    st.title("⚡ Strompreis-Assistent")
    st.write("Willkommen! Diese Anwendung hilft Ihnen, Stromkosten im Haushalt zu sparen.")

    st.divider()

    # 3. Bereich 1: Daten aktualisieren
    st.header("🔄 Daten-Synchronisation")
    if st.button("Aktuelle Strompreise abrufen"):
        with st.spinner("Daten werden geladen..."):
            api_daten = api_client.fetch_current_prices()
            if api_daten:
                db_manager.save_market_prices(api_daten)
                st.success("Erfolgreich: Die aktuellen Strompreise wurden gespeichert!")
            else:
                st.error("Fehler: Es konnten keine Daten abgerufen werden.")

    st.divider()

    # 4. Bereich 2: Berechnung
    st.header("🔌 Günstigste Startzeit berechnen")
    geraet_name = st.text_input("Name des Geräts:", value="Waschmaschine")
    laufzeit = st.number_input("Benötigte Laufzeit (in Stunden):", min_value=1.0, value=2.0, step=1.0)

    if st.button("Beste Startzeit ermitteln"):
        with st.spinner("Berechnung läuft..."):
            api_daten = api_client.fetch_current_prices()
            
            if api_daten:
                empfehlung = analyzer.finde_beste_startzeit(api_daten, laufzeit)
                
                if "fehler" in empfehlung:
                    st.error(empfehlung["fehler"])
                else:
                    st.success(f"💡 Empfehlung für Ihre {geraet_name}:")
                    st.write(f"**Beste Startzeit:** Ab {empfehlung['start_time']} Uhr")
                    st.write(f"**Durchschnittlicher Preis:** {empfehlung['durchschnitt_preis']} Cent/kWh")
            else:
                st.error("Es sind keine Preisdaten vorhanden. Bitte zuerst Preise abrufen!")

if __name__ == "__main__":
    main()