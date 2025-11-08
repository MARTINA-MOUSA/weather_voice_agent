"""
خدمة الطقس
Weather Service
"""

import requests
from typing import Optional, Dict
from config import Config


class WeatherService:
    """خدمة للحصول على معلومات الطقس"""
    
    def __init__(self):
        """تهيئة خدمة الطقس"""
        if not Config.WEATHER_API_KEY:
            raise ValueError("WEATHER_API_KEY غير موجود")
        
        self.api_key = Config.WEATHER_API_KEY
        self.base_url = Config.WEATHER_BASE_URL
    
    def get_weather(self, location: str) -> Optional[Dict]:
        """الحصول على معلومات الطقس لموقع معين"""
        try:
            params = {
                'q': location,
                'appid': self.api_key,
                'units': Config.WEATHER_UNITS,
                'lang': Config.WEATHER_LANG
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"خطأ في جلب بيانات الطقس: {e}")
            return None
    
    def format_weather_response(self, weather_data: Dict) -> str:
        """تنسيق بيانات الطقس إلى رد قابل للقراءة"""
        if not weather_data:
            return "عذراً، لم أتمكن من الحصول على معلومات الطقس في الوقت الحالي."
        
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
        except KeyError as e:
            return f"عذراً، حدث خطأ في معالجة بيانات الطقس: {e}"
    
    def get_weather_info(self, location: str) -> str:
        """الحصول على معلومات الطقس بشكل منسق"""
        weather_data = self.get_weather(location)
        return self.format_weather_response(weather_data)

