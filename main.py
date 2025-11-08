
import sys
import os

# إضافة المجلد الحالي إلى المسار
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from backend.config import Config
from AI.gemini_service import GeminiService
from backend.weather_service import WeatherService
from AI.speech_service import SpeechService

def main():
    """الدالة الرئيسية"""
    try:
        # التحقق من الإعدادات
        Config.validate()
        
        # تهيئة الخدمات
        print("=" * 50)
        print("🌤️ مساعد الطقس الصوتي - جاهز للاستخدام")
        print("=" * 50)
        print("💡 قل 'إنهاء' أو 'خروج' للإنهاء")
        print()
        
        gemini_service = GeminiService()
        weather_service = WeatherService()
        speech_service = SpeechService()
        
        while True:
            try:
                # اختيار طريقة الإدخال
                print("\nاختر طريقة الإدخال:")
                print("1. صوتي (اضغط Enter)")
                print("2. نصي (اكتب 'text' ثم Enter)")
                print("3. خروج (اكتب 'exit' ثم Enter)")
                
                choice = input("\nاختيارك: ").strip().lower()
                
                if choice == 'exit' or choice == '3':
                    print("👋 تم إنهاء البرنامج")
                    break
                
                if choice == 'text' or choice == '2':
                    # إدخال نصي
                    user_input = input("\nاكتب سؤالك: ").strip()
                    if not user_input:
                        continue
                else:
                    # إدخال صوتي
                    print("\n🎤 جارٍ الاستماع... (اضغط Ctrl+C للإلغاء)")
                    user_input = speech_service.listen()
                    
                    if not user_input:
                        print("⚠️ لم يتم التعرف على الصوت. حاول مرة أخرى.\n")
                        continue
                    
                    print(f"✅ تم التعرف على: {user_input}\n")
                
                # التحقق من أوامر الخروج
                if any(word in user_input.lower() for word in ['إنهاء', 'خروج', 'توقف', 'stop', 'exit']):
                    print("👋 تم إنهاء البرنامج")
                    break
                
                # معالجة السؤال
                print("🤔 جارٍ معالجة السؤال...")
                
                # استخراج الموقع
                location = gemini_service.extract_location(user_input)
                
                if location:
                    # الحصول على بيانات الطقس
                    weather_data = weather_service.get_weather(location)
                    
                    if weather_data:
                        response = weather_service.format_weather_response(weather_data)
                    else:
                        response = f"عذراً، لم أتمكن من العثور على معلومات الطقس لـ {location}."
                else:
                    # استخدام Gemini للرد العام
                    response = gemini_service.generate_response(user_input)
                
                print(f"\n💬 الرد: {response}\n")
                
                # اختيار تشغيل الصوت يدوياً
                play_audio = input("هل تريد تشغيل الرد صوتياً؟ (y/n): ").strip().lower()
                if play_audio == 'y' or play_audio == 'yes' or play_audio == 'نعم':
                    speech_service.speak(response)
                
            except KeyboardInterrupt:
                print("\n👋 تم إنهاء البرنامج بواسطة المستخدم")
                break
            except Exception as e:
                error_msg = f"حدث خطأ: {str(e)}"
                print(f" {error_msg}\n")
    
    except ValueError as e:
        print(f" خطأ في الإعدادات: {e}")
        print(" تأكد من إضافة المفاتيح في ملف .env")
    except Exception as e:
        print(f" حدث خطأ: {e}")

if __name__ == "__main__":
    main()
