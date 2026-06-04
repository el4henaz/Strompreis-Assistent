import requests
from datetime import datetime

class AwattarApiClient:
    def __init__(self):
        # آدرس رسمی API وب‌سایت آواتار برای دریافت قیمت‌های بازار
        self.url = "https://api.awattar.de/v1/marketdata"

    def fetch_current_prices(self):
        """دریافت قیمت‌های برق از API و آماده‌سازی داده‌ها"""
        try:
            # ارسال درخواست به API با زمان انتظار حداکثر 10 ثانیه
            response = requests.get(self.url, timeout=10)
            response.raise_for_status() # بررسی اینکه آیا اتصال موفق بوده است
            
            raw_data = response.json()
            market_prices = []
            
            # استخراج و تبدیل فرمت داده‌های خام API
            for item in raw_data.get("data", []):
                # تبدیل زمان لینوکسی (Timestamp) به ساعت خوانا
                start_dt = datetime.fromtimestamp(item["start_timestamp"] / 1000)
                start_hour = start_dt.strftime("%H:00")
                
                # تبدیل قیمت از مگاوات‌ساعت (Eur/MWh) به سنت بر کیلووات‌ساعت (Cent/kWh)
                # فرمول: قیمت خام تقسیم بر 10
                price_eur_mwh = item["marketprice"]
                price_cent_kwh = round(price_eur_mwh / 10, 2)
                
                market_prices.append({
                    "timestamp": item["start_timestamp"],
                    "uhrzeit": start_hour,
                    "preis": price_cent_kwh
                })
                
            return market_prices
            
        except Exception as e:
            print(f"Fehler beim API-Abruf: {e}")
            return None