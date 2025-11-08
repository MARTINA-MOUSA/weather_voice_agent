"""
سكريبت اختبار لـ Weather API
"""

import sys
import os
import io

# إصلاح مشكلة encoding في Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# إضافة المجلد الرئيسي إلى المسار
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from backend.config import Config
from backend.weather_service import WeatherService
from backend.utils.city_mapping import translate_city_name

def test_weather():
    """اختبار Weather API"""
    print("=" * 50)
    print("اختبار Weather API")
    print("=" * 50)
    
    # التحقق من المفتاح
    if not Config.WEATHER_API_KEY:
        print("❌ خطأ: WEATHER_API_KEY غير موجود في ملف .env")
        return False
    
    print(f"✅ المفتاح موجود: {Config.WEATHER_API_KEY[:10]}...")
    
    # اختبار تحويل أسماء المدن
    print("\n📋 اختبار تحويل أسماء المدن:")
    test_cities = ["القاهرة", "القاهره", "Cairo", "دبي", "Dubai"]
    for city in test_cities:
        translated = translate_city_name(city)
        print(f"   {city} -> {translated}")
    
    # تهيئة Weather Service
    try:
        weather_service = WeatherService()
        print("\n✅ تم تهيئة Weather Service بنجاح")
    except Exception as e:
        print(f"❌ خطأ في تهيئة Weather Service: {e}")
        return False
    
    # اختبار البحث عن القاهرة
    print("\n🧪 اختبار البحث عن القاهرة:")
    test_locations = ["Cairo", "Cairo,EG", "القاهرة", "القاهره"]
    
    for loc in test_locations:
        print(f"\n   جارٍ البحث عن: {loc}")
        weather_data = weather_service.get_weather(loc)
        
        if weather_data:
            print(f"   ✅ نجح!")
            print(f"   المدينة: {weather_data.get('name', 'غير معروف')}")
            print(f"   الدولة: {weather_data.get('sys', {}).get('country', 'غير معروف')}")
            print(f"   الحرارة: {weather_data.get('main', {}).get('temp', 'غير معروف')}°C")
            return True
        else:
            print(f"   ❌ فشل")
    
    print("\n❌ فشل في العثور على معلومات الطقس للقاهرة")
    print("\n💡 الحلول المقترحة:")
    print("   1. تحقق من صحة WEATHER_API_KEY في ملف .env")
    print("   2. تحقق من اتصال الإنترنت")
    print("   3. جرب استخدام 'Cairo,EG' مباشرة")
    
    return False

if __name__ == "__main__":
    test_weather()

