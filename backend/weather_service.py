
import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import requests
from typing import Optional, Dict
from backend.config import Config
from backend.utils.city_mapping import translate_city_name


class WeatherService:
    
    def __init__(self):
        if not Config.WEATHER_API_KEY:
            raise ValueError("WEATHER_API_KEY is missing")
        
        self.api_key = Config.WEATHER_API_KEY
        self.base_url = Config.WEATHER_BASE_URL
    
    def get_weather(self, location: str) -> Optional[Dict]:
        if not location:
            return None
        
        # تنظيف الموقع
        location = location.strip()
        
        # تحويل اسم المدينة من العربية إلى الإنجليزية
        english_location = translate_city_name(location)
        
        # محاولة البحث بالاسم الإنجليزي أولاً، ثم الأصلي
        locations_to_try = [english_location, location]
        
        # إضافة "Cairo,EG" للقاهرة كحل احتياطي
        if "cairo" in location.lower() or "القاهرة" in location or "القاهره" in location:
            locations_to_try.insert(0, "Cairo,EG")
        
        for loc in locations_to_try:
            if not loc:
                continue
            try:
                params = {
                    'q': loc,
                    'appid': self.api_key,
                    'units': Config.WEATHER_UNITS,
                    'lang': Config.WEATHER_LANG
                }
                response = requests.get(self.base_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    # جرب الاسم التالي
                    continue
                else:
                    # خطأ آخر
                    response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                # إذا كان الخطأ 404، جرب الاسم الآخر
                if e.response and e.response.status_code == 404:
                    continue
                else:
                    # خطأ آخر غير 404
                    continue
            except requests.exceptions.RequestException:
                # خطأ في الاتصال، جرب الاسم الآخر
                continue
        
        # فشلت جميع المحاولات
        return None
    
    def format_weather_response(self, weather_data: Dict) -> str:
        if not weather_data:
            return "Sorry, unable to get weather information at this time."
        
        try:
            city = weather_data['name']
            country = weather_data['sys']['country']
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            wind_speed = weather_data.get('wind', {}).get('speed', 0)
            pressure = weather_data['main'].get('pressure', 0)
            
            response = f"""🌤️ الطقس في {city}، {country}:

🌡️ الحرارة: {temp}°C
🌡️ الشعور: {feels_like}°C
💧 الرطوبة: {humidity}%
☁️ الحالة: {description}
💨 سرعة الرياح: {wind_speed} م/ث
📊 الضغط: {pressure} hPa"""
            
            return response
        except KeyError:
            return "Error: Failed to process weather data."
    
    def get_weather_info(self, location: str) -> str:
        weather_data = self.get_weather(location)
        return self.format_weather_response(weather_data)

