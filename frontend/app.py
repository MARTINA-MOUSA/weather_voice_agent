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
from backend.utils.helpers import format_weather_card

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

def display_weather_card(weather_data: dict):
    """عرض بطاقة الطقس"""
    if not weather_data:
        return
    
    card_data = format_weather_card(weather_data)
    
    if not card_data:
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🌡️ الحرارة", f"{card_data['temperature']}°C")
        st.metric("🌡️ الشعور", f"{card_data['feels_like']}°C")
    
    with col2:
        st.metric("💧 الرطوبة", f"{card_data['humidity']}%")
        st.metric("💨 الرياح", f"{card_data['wind_speed']} م/ث")
    
    with col3:
        st.metric("📊 الضغط", f"{card_data['pressure']} hPa")
        st.metric("☁️ الحالة", card_data['description'])

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
                st.rerun()
        
        st.markdown("---")
        
        # وضع الصوت
        voice_mode = st.checkbox("🎤 تفعيل الوضع الصوتي", value=False)
        
        if voice_mode:
            st.info("💡 اضغط على زر '🎤 تحدث' للبدء")
        
        st.markdown("---")
        st.header("📝 أمثلة على الأسئلة")
        st.markdown("""
        - ما هو الطقس في القاهرة؟
        - كيف الطقس اليوم في دبي؟
        - أخبرني عن الطقس في الرياض
        - ما هي درجة الحرارة في لندن؟
        """)
        
        st.markdown("---")
        if st.button("🗑️ مسح المحادثة"):
            st.session_state.messages = []
            st.session_state.weather_data = None
            st.rerun()
    
    # التحقق من التهيئة
    if not st.session_state.initialized:
        st.warning("⚠️ يرجى تهيئة التطبيق من الشريط الجانبي أولاً")
        return
    
    # منطقة المحادثة
    st.header("💬 المحادثة")
    
    # عرض الرسائل السابقة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # التحقق من وجود إدخال صوتي معلق
    pending_voice = st.session_state.get('pending_voice_input', None)
    
    # زر الصوت
    if voice_mode:
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🎤 تحدث", use_container_width=True):
                with st.spinner("🎤 جارٍ الاستماع..."):
                    voice_input = st.session_state.speech_service.listen()
                    if voice_input:
                        # حفظ الإدخال الصوتي للمعالجة
                        st.session_state.pending_voice_input = voice_input
                        st.rerun()
                    else:
                        st.warning("⚠️ لم يتم التعرف على الصوت. حاول مرة أخرى.")
    
    # إدخال النص
    text_input = st.chat_input("اكتب سؤالك هنا...")
    
    # استخدام الإدخال الصوتي المعلق أو النصي
    user_input = pending_voice if pending_voice else text_input
    
    if user_input:
        # إضافة رسالة المستخدم
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # مسح الإدخال الصوتي المعلق بعد استخدامه
        if pending_voice:
            st.session_state.pending_voice_input = None
        
        # معالجة السؤال وعرض الرد
        with st.chat_message("assistant"):
            with st.spinner("🤔 جارٍ التفكير..."):
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
                    
                    # عرض الرد
                    st.write(response)
                    
                    # إضافة رد المساعد إلى الرسائل
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                    # تشغيل الصوت تلقائياً إذا كان الوضع الصوتي مفعلاً
                    if voice_mode and st.session_state.speech_service and (st.session_state.speech_service.use_edge_tts or st.session_state.speech_service.use_gtts or st.session_state.speech_service.tts_engine):
                        try:
                            # تشغيل الصوت في thread منفصل لتجنب تعطيل الواجهة
                            import threading
                            speech_service = st.session_state.speech_service  # نسخ المرجع قبل thread
                            
                            def speak_async(service, text):
                                service.speak(text)
                            
                            thread = threading.Thread(target=speak_async, args=(speech_service, response))
                            thread.daemon = True
                            thread.start()
                        except Exception as e:
                            print(f"خطأ في تشغيل الصوت: {e}")
                    
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
                    
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    
    # عرض بيانات الطقس
    if st.session_state.weather_data:
        st.markdown("---")
        st.header("📊 تفاصيل الطقس")
        display_weather_card(st.session_state.weather_data)
        
        # إضافة معلومات إضافية
        card_data = format_weather_card(st.session_state.weather_data)
        if card_data:
            st.markdown("### 📍 الموقع")
            st.info(f"**{card_data['city']}، {card_data['country']}**")
            
            # أيقونة الطقس
            if card_data.get('icon'):
                icon_url = f"http://openweathermap.org/img/wn/{card_data['icon']}@2x.png"
                st.image(icon_url, width=100)
        
        # زر تشغيل الصوت يدوياً
        if st.session_state.speech_service and (st.session_state.speech_service.use_edge_tts or st.session_state.speech_service.use_gtts or st.session_state.speech_service.tts_engine):
            st.markdown("---")
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🔊 تشغيل آخر رد صوتياً", use_container_width=True):
                    last_message = None
                    for msg in reversed(st.session_state.messages):
                        if msg["role"] == "assistant":
                            last_message = msg["content"]
                            break
                    if last_message:
                        try:
                            import threading
                            speech_service = st.session_state.speech_service  # نسخ المرجع قبل thread
                            
                            def speak_async(service, text):
                                service.speak(text)
                            
                            thread = threading.Thread(target=speak_async, args=(speech_service, last_message))
                            thread.daemon = True
                            thread.start()
                            st.success("🔊 جارٍ تشغيل الصوت...")
                        except Exception as e:
                            st.error(f"⚠️ خطأ في تشغيل الصوت: {str(e)}")
                    else:
                        st.warning("⚠️ لا يوجد رد للقراءة")

if __name__ == "__main__":
    main()

