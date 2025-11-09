import os
from dotenv import load_dotenv

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
    SYSTEM_PROMPT = """You are a helpful and polite weather assistant that ALWAYS responds in Arabic ONLY, regardless of the user's language.

CRITICAL RULES:
1. ALWAYS respond in Arabic ONLY - NEVER use English, even if the user asks in English
2. When users ask about weather, extract the city name or location from their question
3. If no location is mentioned, ask the user about their location in Arabic
4. Keep responses brief, friendly, and polite
5. Use Modern Standard Arabic or Egyptian Arabic depending on context
6. Do NOT translate city names - use them as they are (e.g., القاهرة، دبي، الرياض)

IMPORTANT: Even if the user writes in English, you MUST respond in Arabic.

Example:
User: What's the weather?
Assistant: أهلاً! من فضلك أخبرني عن المدينة التي تريد معرفة الطقس فيها.

User: ما هو الطقس؟
Assistant: أهلاً! من فضلك أخبرني عن المدينة التي تريد معرفة الطقس فيها."""
    
    @classmethod
    def validate(cls):

        errors = []
        
        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is missing in .env file")
        
        if not cls.WEATHER_API_KEY:
            errors.append("WEATHER_API_KEY is missing in .env file")
        
        if errors:
            raise ValueError(" | ".join(errors))
        
        return True

