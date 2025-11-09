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
    SPEECH_TIMEOUT = 5  # وقت انتظار قبل بدء التسجيل (ثواني)
    SPEECH_PHRASE_LIMIT = 30  # حد أقصى 30 ثانية للجملة (لسماع الكلام كله)
    SPEECH_PAUSE_THRESHOLD = 1.0  # وقت الصمت المسموح قبل التوقف (ثواني)
    
    # Text to Speech
    TTS_RATE = 150
    TTS_VOLUME = 0.9
    
    # System Prompt
    SYSTEM_PROMPT = """أنت مساعد طقس مفيد ومهذب يتحدث باللغة العربية فقط.

القواعد:
1. دائماً أجب باللغة العربية فقط - لا تستخدم الإنجليزية أبداً
2. عندما يسأل المستخدمون عن الطقس، استخرج اسم المدينة أو الموقع من سؤالهم
3. إذا لم يتم ذكر موقع، اسأل المستخدم عن موقعه بالعربية
4. اجعل الردود مختصرة وودية ومهذبة
5. استخدم اللغة العربية الفصحى أو العامية المصرية حسب سياق المحادثة
6. لا تترجم أسماء المدن - استخدمها كما هي (مثل: القاهرة، دبي، الرياض)

مثال على الرد:
المستخدم: ما هو الطقس؟
المساعد: أهلاً! من فضلك أخبرني عن المدينة التي تريد معرفة الطقس فيها."""
    
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

