import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="daten.db"):
        self.db_name = db_name
        self.init_database()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_database(self):
        """ساخت جدول‌های مورد نیاز در صورت عدم وجود"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # جدول اول: ذخیره قیمت‌های برق بازار بورس
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS marktplatz_preise (
                    timestamp INTEGER PRIMARY KEY,
                    uhrzeit TEXT,
                    preis REAL
                )
            """)
            # جدول دوم: ذخیره اطلاعات دستگاه‌ها و شبیه‌سازی مصرف
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS geraete_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    geraet_name TEXT,
                    leistung REAL,
                    laufzeit REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_market_prices(self, price_list):
        """ذخیره قیمت‌های دریافت شده در دیتابیس"""
        if not price_list:
            return
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for item in price_list:
                cursor.execute("""
                    INSERT OR REPLACE INTO marktplatz_preise (timestamp, uhrzeit, preis)
                    VALUES (?, ?, ?)
                """, (item["timestamp"], item["uhrzeit"], item["preis"]))
            conn.commit()

    def insert_device(self, name, leistung, laufzeit):
        """ثبت دستگاه محاسبه شده در دیتابیس"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO geraete_log (geraet_name, leistung, laufzeit)
                VALUES (?, ?, ?)
            """, (name, leistung, laufzeit))
            conn.commit()