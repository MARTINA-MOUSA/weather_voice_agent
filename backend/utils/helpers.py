"""
وظائف مساعدة
Helper functions
"""

from typing import Dict, Optional


def format_weather_card(weather_data: Dict) -> Dict:
    """تنسيق بيانات الطقس لعرضها في بطاقة"""
    if not weather_data:
        return {}
    
    try:
        return {
            'city': weather_data.get('name', 'غير معروف'),
            'country': weather_data.get('sys', {}).get('country', ''),
            'temperature': weather_data.get('main', {}).get('temp', 0),
            'feels_like': weather_data.get('main', {}).get('feels_like', 0),
            'humidity': weather_data.get('main', {}).get('humidity', 0),
            'description': weather_data.get('weather', [{}])[0].get('description', ''),
            'wind_speed': weather_data.get('wind', {}).get('speed', 0),
            'pressure': weather_data.get('main', {}).get('pressure', 0),
            'icon': weather_data.get('weather', [{}])[0].get('icon', ''),
        }
    except Exception as e:
        print(f"خطأ في تنسيق بيانات الطقس: {e}")
        return {}


def validate_location(location: str) -> bool:
    """التحقق من صحة اسم الموقع"""
    if not location or len(location.strip()) < 2:
        return False
    return True

