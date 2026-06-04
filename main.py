import streamlit as st
import os
import sys

# مطمئن شدن از شناخت مسیر پوشه core در زمان اجرای استریم‌لیت
aktueller_pfad = os.path.dirname(os.path.abspath(__file__))
if aktueller_pfad not in sys.path:
    sys.path.insert(0, aktueller_pfad)

from core.api_client import AwattarApiClient
from core.database import DatabaseManager
from core.analyzer import StrompreisAnalyzer

def main():
    # ساخت آبجکت‌های اصلی
    api_client = AwattarApiClient()
    db_manager = DatabaseManager()
    analyzer = StrompreisAnalyzer()

    # تنظیمات صفحه وب
    st.set_page_config(page_title="Strompreis-Assistent", page_icon="⚡", layout="centered")

    # هدر اصلی برنامه
    st.title("⚡ Strompreis-Assistent")
    st.write("Willkommen! Diese Anwendung hilft Ihnen, Stromkosten im Haushalt zu sparen.")
    
    st.divider()

    # بخش اول: دریافت داده‌ها
    st.header("🔄 Daten-Synchronisation")
    st.write("Verbindet sich mit der aWATTar-API, um die aktuellen Preise abzurufen.")
    
    if st.button("Aktuelle Strompreise abrufen", type="primary"):
        with st.spinner("Daten werden geladen..."):
            api_daten = api_client.fetch_current_prices()
            if api_daten:
                db_manager.save_market_prices(api_daten)
                st.success("✅ Erfolgreich: Die aktuellen Strompreise wurden gespeichert!")
            else:
                st.error("❌ Fehler: Es konnten keine Daten abgerufen werden.")

    st.divider()

    # بخش دوم: فرم محاسبه دستگاه‌ها با منوی کشویی
    st.header("🔌 Günstigste Startzeit berechnen")
    st.write("Wählen Sie ein Haushaltsgerät aus, um die beste Startzeit zu ermitteln.")

    # تعریف لیست دستگاه‌ها به همراه توان مصرفی پیش‌فرض آن‌ها (به کیلووات - kW)
    geraete_daten = {
        "Waschmaschine": {"leistung": 2.0, "laufzeit": 2.0},
        "Geschirrspüler": {"leistung": 1.5, "laufzeit": 3.0},
        "Wäschetrockner": {"leistung": 2.5, "laufzeit": 2.0},
        "Backofen": {"leistung": 3.0, "laufzeit": 1.0},
        "Elektroauto": {"leistung": 11.0, "laufzeit": 4.0},
        "Wärmepumpe": {"leistung": 5.0, "laufzeit": 5.0},
        "Staubsauger": {"leistung": 0.8, "laufzeit": 1.0}
    }

    # ۱. منوی کشویی برای انتخاب دستگاه
    auswahl_geraet = st.selectbox(
        "Wählen Sie ein Gerät aus:",
        options=list(geraete_daten.keys())
    )

    # استخراج اطلاعات پیش‌فرض دستگاه انتخاب شده
    standard_leistung = geraete_daten[auswahl_geraet]["leistung"]
    standard_laufzeit = geraete_daten[auswahl_geraet]["laufzeit"]

    # ۲. فیلدهای ورودی که بر اساس دستگاه انتخاب شده، مقدار پیش‌فرضشان تغییر می‌کند
    laufzeit = st.number_input(
        "Benoetigte Laufzeit (in Stunden):",
        min_value=1.0, 
        max_value=24.0, 
        value=standard_laufzeit, 
        step=1.0
    )
    
    # نمایش توان مصرفی دستگاه به کاربر جهت اطلاع
    st.caption(f"ℹ️ Geschätzte Leistung für dieses Gerät: {standard_leistung} kW")

    if st.button("Beste Startzeit ermitteln"):
        with st.spinner("Berechnung läuft..."):
            api_daten = api_client.fetch_current_prices()
            
            if api_daten:
                empfehlung = analyzer.finde_beste_startzeit(api_daten, laufzeit)
                
                if "fehler" in empfehlung:
                    st.error(empfehlung["fehler"])
                else:
                    st.success(f"💡 Empfehlung für Ihre {auswahl_geraet}:")
                    
                    # نمایش نتایج به صورت کارت‌های زیبا (Metrics)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="Beste Startzeit", value=f"Ab {empfehlung['start_time']} Uhr")
                    with col2:
                        st.metric(label="Durchschnittlicher Preis", value=f"{empfehlung['durchschnitt_preis']} Cent/kWh")
                    
                    # محاسبه هزینه تقریبی مصرف این دستگاه
                    gesamtkosten = round((standard_leistung * laufzeit * empfehlung['durchschnitt_preis']) / 100, 2)
                    st.info(f"💰 Geschätzte Gesamtkosten für diesen Lauf: ca. {gesamtkosten} €")
                    
                    # ذخیره تاریخچه دقیق این محاسبه در دیتابیس
                    db_manager.insert_device(auswahl_geraet, standard_leistung, laufzeit)
            else:
                st.error("❌ Keine Preisdaten vorhanden. Bitte zuerst Preise abrufen!")

if __name__ == "__main__":
    main()