"""
تطبيق Streamlit الرئيسي
Main Streamlit Application
"""

import sys
import os

# إضافة المجلد الرئيسي إلى المسار
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
import time
from typing import Optional
from backend.config import Config
from AI.gemini_service import GeminiService
from backend.weather_service import WeatherService
from AI.speech_service import SpeechService
# format_weather_card لم يعد مستخدماً

# إعدادات الصفحة
st.set_page_config(
    page_title="مساعد الطقس الصوتي",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .weather-card {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #1e3c72;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #2a5298;
    }
    .voice-indicator {
        display: inline-block;
        animation: pulse 1.5s ease-in-out infinite;
        color: #1e3c72;
        font-size: 1.2rem;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    .recording-indicator {
        display: inline-block;
        animation: blink 1s ease-in-out infinite;
        color: #dc3545;
        font-size: 1.5rem;
        font-weight: bold;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
</style>
""", unsafe_allow_html=True)

# تهيئة الجلسة
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.messages = []
    st.session_state.weather_data = None
    st.session_state.gemini_service = None
    st.session_state.weather_service = None
    st.session_state.speech_service = None
    st.session_state.pending_voice_input = None
    st.session_state.is_voice_input = False  # للتمييز بين الإدخال الصوتي والنصي
    st.session_state.last_voice_response = None  # حفظ آخر رد صوتي
    st.session_state.is_recording = False  # حالة التسجيل
    st.session_state.is_speaking = False  # حالة الرد الصوتي

def main():
    """الدالة الرئيسية للتطبيق"""
    
    # العنوان الرئيسي
    st.markdown("""
    <div class="main-header">
        <h1>🌤️ مساعد الطقس الصوتي</h1>
        <p>اسأل عن الطقس في أي مكان في العالم</p>
    </div>
    """, unsafe_allow_html=True)
    
    # الشريط الجانبي
    with st.sidebar:
        st.header("⚙️ الإعدادات")
        
        # تهيئة الخدمات يدوياً
        if not st.session_state.initialized:
            if st.button("🚀 تهيئة التطبيق", use_container_width=True):
                try:
                    Config.validate()
                    st.session_state.gemini_service = GeminiService()
                    st.session_state.weather_service = WeatherService()
                    st.session_state.speech_service = SpeechService()
                    st.session_state.initialized = True
                    
                    # التحقق من محرك الصوت
                    if st.session_state.speech_service.use_gtts and st.session_state.speech_service.pygame_available:
                        st.success("✅ تم تهيئة التطبيق بنجاح! 🔊 الصوت متاح (gTTS + pygame - تشغيل مباشر من الذاكرة بدون ملفات)")
                    elif st.session_state.speech_service.use_edge_tts:
                        st.success("✅ تم تهيئة التطبيق بنجاح! 🔊 الصوت متاح (edge-tts - يدعم العربية)")
                    elif st.session_state.speech_service.use_gtts:
                        st.success("✅ تم تهيئة التطبيق بنجاح! 🔊 الصوت متاح (gTTS - يدعم العربية)")
                    elif st.session_state.speech_service.tts_engine:
                        st.success("✅ تم تهيئة التطبيق بنجاح! 🔊 الصوت متاح (pyttsx3)")
                    else:
                        st.warning("✅ تم تهيئة التطبيق بنجاح! ⚠️ محرك الصوت غير متاح - قم بتثبيت: pip install gtts pygame")
                    
                    st.rerun()
                except ValueError as e:
                    st.error(f"❌ خطأ في الإعدادات: {e}")
        else:
            st.success("✅ التطبيق جاهز")
            if st.button("🔄 إعادة التهيئة", use_container_width=True):
                st.session_state.initialized = False
                st.session_state.messages = []
                st.session_state.weather_data = None
                st.session_state.gemini_service = None
                st.session_state.weather_service = None
                st.session_state.speech_service = None
                st.session_state.last_voice_response = None
                st.rerun()
        
        st.markdown("---")
        st.header("📝 أمثلة على الأسئلة")
        st.markdown("""
        - ما هو الطقس في القاهرة؟
        - كيف الطقس اليوم في دبي؟
        - أخبرني عن الطقس في الرياض
        - ما هي درجة الحرارة في لندن؟
        """)
        
        st.markdown("---")
        if st.button("🗑️ مسح المحادثة", use_container_width=True):
            st.session_state.messages = []
            st.session_state.weather_data = None
            st.session_state.last_voice_response = None
            st.session_state.is_recording = False
            st.session_state.is_speaking = False
            st.rerun()
    
    # التحقق من التهيئة
    if not st.session_state.initialized:
        st.warning("⚠️ يرجى تهيئة التطبيق من الشريط الجانبي أولاً")
        return
    
    # منطقة المحادثة - مثل ChatGPT
    # عرض الرسائل السابقة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            # إذا كان هناك رد صوتي، عرض علامة AI صوتية (فقط إذا انتهى الصوت)
            if message.get("is_voice_response", False) and not st.session_state.get('is_speaking', False):
                st.markdown('<span class="voice-indicator">🔊</span> *تم الرد صوتياً*', unsafe_allow_html=True)
    
    # مؤشر التسجيل الصوتي
    if st.session_state.get('is_recording', False):
        st.markdown('<div class="recording-indicator">🎤 جارٍ التسجيل...</div>', unsafe_allow_html=True)
    
    # مؤشر الرد الصوتي (يظهر فقط أثناء الرد)
    if st.session_state.get('is_speaking', False):
        st.markdown('<div class="voice-indicator">🔊 جاري الرد صوتياً...</div>', unsafe_allow_html=True)
        # تحديث تلقائي للواجهة أثناء الرد (كل ثانية)
        import time
        time.sleep(1)
        # إعادة تحميل الصفحة لتحديث الحالة
        if st.session_state.get('is_speaking', False):
            st.rerun()
    
    # التحقق من وجود إدخال صوتي معلق
    pending_voice = st.session_state.get('pending_voice_input', None)
    
    # منطقة الإدخال في الأسفل - مثل ChatGPT
    # زر التسجيل الصوتي بجانب chat_input
    input_col1, input_col2 = st.columns([1, 20])
    
    with input_col1:
        # زر التسجيل الصوتي
        if st.button("🎤", use_container_width=True, help="اضغط للتسجيل الصوتي - سيتم الرد صوتياً", key="mic_button"):
            st.session_state.is_recording = True
            st.rerun()
    
    # معالجة التسجيل الصوتي
    if st.session_state.get('is_recording', False) and not pending_voice:
        with st.spinner("🎤 جارٍ الاستماع..."):
            voice_input = st.session_state.speech_service.listen()
            st.session_state.is_recording = False
            if voice_input:
                # حفظ الإدخال الصوتي للمعالجة
                st.session_state.pending_voice_input = voice_input
                st.session_state.is_voice_input = True  # تمييز الإدخال الصوتي
                st.rerun()
            else:
                st.warning("⚠️ لم يتم التعرف على الصوت. حاول مرة أخرى.")
    
    with input_col2:
        # إدخال النص (Send button)
        text_input = st.chat_input("اكتب سؤالك هنا أو اضغط 🎤 للتسجيل الصوتي...")
    
    # استخدام الإدخال الصوتي المعلق أو النصي
    user_input = pending_voice if pending_voice else text_input
    
    if user_input:
        is_voice = st.session_state.is_voice_input if pending_voice else False
        
        # إضافة رسالة المستخدم (في كل الحالات)
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # مسح الإدخال الصوتي المعلق بعد استخدامه
        if pending_voice:
            st.session_state.pending_voice_input = None
            st.session_state.is_voice_input = False
        
        # معالجة السؤال
        try:
            # استخراج الموقع
            location = st.session_state.gemini_service.extract_location(user_input)
            
            if location:
                # الحصول على بيانات الطقس
                weather_data = st.session_state.weather_service.get_weather(location)
                
                if weather_data:
                    st.session_state.weather_data = weather_data
                    response = st.session_state.weather_service.format_weather_response(weather_data)
                else:
                    # محاولة البحث مرة أخرى بأسماء بديلة
                    from backend.utils.city_mapping import translate_city_name
                    english_name = translate_city_name(location)
                    
                    # محاولة البحث بالاسم الإنجليزي
                    if english_name != location:
                        weather_data = st.session_state.weather_service.get_weather(english_name)
                        if weather_data:
                            st.session_state.weather_data = weather_data
                            response = st.session_state.weather_service.format_weather_response(weather_data)
                        else:
                            # محاولة مع رمز الدولة للقاهرة
                            if "cairo" in location.lower() or "القاهرة" in location or "القاهره" in location:
                                weather_data = st.session_state.weather_service.get_weather("Cairo,EG")
                                if weather_data:
                                    st.session_state.weather_data = weather_data
                                    response = st.session_state.weather_service.format_weather_response(weather_data)
                                else:
                                    response = f"عذراً، لم أتمكن من العثور على معلومات الطقس لـ {location}. يرجى التحقق من اسم المدينة أو المفتاح."
                            else:
                                response = f"عذراً، لم أتمكن من العثور على معلومات الطقس لـ {location}. يرجى التحقق من اسم المدينة."
                    else:
                        response = f"عذراً، لم أتمكن من العثور على معلومات الطقس لـ {location}. يرجى التحقق من اسم المدينة أو المفتاح."
            else:
                # استخدام Gemini للرد العام
                response = st.session_state.gemini_service.generate_response(user_input)
            
            # إذا كان الإدخال صوتي: تشغيل الصوت مباشرة مع عرض علامة AI صوتية
            if is_voice:
                # حفظ الرد للاستخدام لاحقاً
                st.session_state.last_voice_response = response
                
                # إضافة رد المساعد مع علامة صوتية
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "is_voice_response": True  # علامة للرد الصوتي
                })
                
                # عرض الرسائل الجديدة
                with st.chat_message("user"):
                    st.write(user_input)
                
                with st.chat_message("assistant"):
                    st.write(response)
                    # لا نعرض علامة "تم الرد" هنا - سنعرضها بعد انتهاء الصوت
                
                # تفعيل مؤشر الرد الصوتي
                st.session_state.is_speaking = True
                
                # تشغيل الصوت مباشرة في thread منفصل
                import threading
                speech_service = st.session_state.speech_service
                
                def speak_async(service, text):
                    try:
                        service.speak(text)
                    finally:
                        # إيقاف المؤشر بعد انتهاء الصوت
                        import time
                        time.sleep(0.5)  # انتظار قصير للتأكد من انتهاء الصوت
                        # تحديث الحالة بدون استخدام st.rerun() في thread
                        st.session_state.is_speaking = False
                
                thread = threading.Thread(target=speak_async, args=(speech_service, response))
                thread.daemon = True
                thread.start()
                
                st.rerun()
            else:
                # إذا كان الإدخال نصي: عرض النص فقط
                with st.chat_message("assistant"):
                    st.write(response)
                    
                    # إضافة رد المساعد إلى الرسائل
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "is_voice_response": False
                    })
                    
        except Exception as e:
            error_str = str(e)
            # تحويل الأخطاء الإنجليزية إلى عربية
            if "404" in error_str or "not found" in error_str.lower():
                error_msg = "عذراً، حدث خطأ في الاتصال بخدمة الذكاء الاصطناعي. يرجى المحاولة مرة أخرى."
            elif "quota" in error_str.lower() or "limit" in error_str.lower():
                error_msg = "عذراً، تم تجاوز الحد المسموح من الاستخدام. يرجى المحاولة لاحقاً."
            elif "GEMINI_API_KEY" in error_str or "WEATHER_API_KEY" in error_str:
                error_msg = "عذراً، يرجى التحقق من إعدادات المفاتيح في ملف .env"
            else:
                error_msg = "عذراً، حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى."
            
            # عرض الخطأ فقط إذا كان الإدخال نصي
            if not is_voice:
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
            else:
                # إذا كان صوتي، نطق الخطأ
                import threading
                speech_service = st.session_state.speech_service
                def speak_async(service, text):
                    service.speak(text)
                thread = threading.Thread(target=speak_async, args=(speech_service, error_msg))
                thread.daemon = True
                thread.start()
    
    # لا نعرض تفاصيل الطقس منفصلة - كل شيء في المحادثة
        

if __name__ == "__main__":
    main()

