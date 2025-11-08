"""
سكريبت اختبار لـ Gemini API
"""

import sys
import os

# إضافة المجلد الرئيسي إلى المسار
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from backend.config import Config
import google.generativeai as genai

def test_gemini():
    """اختبار اتصال Gemini"""
    try:
        print("=" * 50)
        print("اختبار اتصال Gemini API")
        print("=" * 50)
        
        # التحقق من المفتاح
        if not Config.GEMINI_API_KEY:
            print("❌ خطأ: GEMINI_API_KEY غير موجود في ملف .env")
            return False
        
        print(f"✅ المفتاح موجود: {Config.GEMINI_API_KEY[:10]}...")
        print(f"📋 النموذج المحدد: {Config.GEMINI_MODEL}")
        
        # تهيئة Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # محاولة سرد النماذج المتاحة
        print("\n📋 جارٍ جلب النماذج المتاحة...")
        try:
            models = genai.list_models()
            available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
            print(f"✅ النماذج المتاحة: {len(available_models)}")
            for model in available_models[:5]:  # عرض أول 5 نماذج
                print(f"   - {model}")
        except Exception as e:
            print(f"⚠️ لم يتمكن من جلب النماذج: {e}")
        
        # اختبار النموذج المحدد
        print(f"\n🧪 اختبار النموذج: {Config.GEMINI_MODEL}")
        try:
            model = genai.GenerativeModel(Config.GEMINI_MODEL)
            response = model.generate_content("مرحباً، اكتب 'نجح' فقط")
            
            if response and hasattr(response, 'text'):
                print(f"✅ نجح! الرد: {response.text.strip()}")
                return True
            else:
                print("❌ خطأ: لم يتم الحصول على رد صحيح")
                return False
        except Exception as e:
            error_str = str(e)
            print(f"❌ خطأ في استخدام النموذج: {error_str}")
            
            # اقتراحات
            if "404" in error_str or "not found" in error_str.lower():
                print("\n💡 الحلول المقترحة:")
                print("   1. جرب استخدام 'gemini-pro' بدلاً من 'gemini-1.5-flash'")
                print("   2. أو جرب 'gemini-1.5-pro'")
                print("   3. تحقق من أن المفتاح صحيح وله صلاحيات الوصول")
            
            return False
            
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        return False

if __name__ == "__main__":
    test_gemini()

