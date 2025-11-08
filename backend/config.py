import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

class Config:
    
    # Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-2.5-flash" 
    # Weather API
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    WEATHER_UNITS = "metric"
    WEATHER_LANG = "ar"
    
    # Speech Recognition
    SPEECH_LANGUAGE = "ar-EG"
    SPEECH_TIMEOUT = 5
    SPEECH_PHRASE_LIMIT = 10
    
    # Text to Speech
    TTS_RATE = 150
    TTS_VOLUME = 0.9
    
    # System Prompt
    SYSTEM_PROMPT = """أنت مساعد طقس مفيد ومهذب.
    عندما يسأل المستخدمون عن الطقس، استخرج اسم المدينة أو الموقع من سؤالهم.
    أجب بشكل طبيعي ومحادثة باللغة العربية.
    إذا لم يتم ذكر موقع، اسأل المستخدم عن موقعه.
    اجعل الردود مختصرة وودية."""
    
    @classmethod
    def validate(cls):
        """التحقق من صحة الإعدادات"""
        errors = []
        
        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY غير موجود في ملف .env")
        
        if not cls.WEATHER_API_KEY:
            errors.append("WEATHER_API_KEY غير موجود في ملف .env")
        
        if errors:
            raise ValueError(" | ".join(errors))
        
        return True

