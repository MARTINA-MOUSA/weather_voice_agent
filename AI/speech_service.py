
import sys
import os
import tempfile
import threading

# إضافة المجلد الرئيسي إلى المسار
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import speech_recognition as sr
from typing import Optional
from backend.config import Config

# محاولة استيراد gTTS (الأفضل للعربية)
try:
    from gtts import gTTS
    import playsound
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# محاولة استيراد pyttsx3 كبديل
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class SpeechService:
    
    def __init__(self):
        # تهيئة التعرف على الصوت
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # تهيئة تحويل النص إلى كلام
        self.use_gtts = GTTS_AVAILABLE  # استخدام gTTS إذا كان متاحاً (يدعم العربية)
        self.tts_engine = None
        
        if not self.use_gtts and PYTTSX3_AVAILABLE:
            # استخدام pyttsx3 كبديل
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', Config.TTS_RATE)
                self.tts_engine.setProperty('volume', Config.TTS_VOLUME)
            except Exception:
                self.tts_engine = None
    
    def listen(self, timeout: int = None, phrase_time_limit: int = None) -> Optional[str]:
        """الاستماع إلى إدخال المستخدم الصوتي"""
        try:
            timeout = timeout or Config.SPEECH_TIMEOUT
            phrase_time_limit = phrase_time_limit or Config.SPEECH_PHRASE_LIMIT
            
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            text = self.recognizer.recognize_google(
                audio, 
                language=Config.SPEECH_LANGUAGE
            )
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            # لا نطبع الأخطاء للمستخدم
            return None
        except Exception:
            # لا نطبع الأخطاء للمستخدم
            return None
    
    def speak(self, text: str):
        """تحويل النص إلى كلام"""
        if not text or not text.strip():
            return
        
        # تنظيف النص من الرموز التي قد تسبب مشاكل
        clean_text = text.replace("🌤️", "").replace("🌡️", "").replace("💧", "").replace("☁️", "").replace("💨", "").replace("📊", "").replace("📍", "").strip()
        
        if not clean_text:
            return
        
        # استخدام gTTS للعربية (الأفضل)
        if self.use_gtts:
            try:
                # إنشاء ملف صوتي مؤقت
                tts = gTTS(text=clean_text, lang='ar', slow=False)
                
                # حفظ في ملف مؤقت
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tmp_file_path = tmp_file.name
                    tts.save(tmp_file_path)
                
                # تشغيل الملف
                try:
                    playsound.playsound(tmp_file_path, block=True)
                except Exception:
                    # إذا فشل playsound، جرب طريقة أخرى
                    import subprocess
                    import platform
                    if platform.system() == 'Windows':
                        subprocess.run(['start', tmp_file_path], shell=True, check=False)
                    elif platform.system() == 'Darwin':
                        subprocess.run(['afplay', tmp_file_path], check=False)
                    else:
                        subprocess.run(['mpg123', tmp_file_path], check=False)
                
                # حذف الملف المؤقت
                try:
                    os.unlink(tmp_file_path)
                except:
                    pass
                    
            except Exception as e:
                print(f"خطأ في gTTS: {e}")
                # محاولة استخدام pyttsx3 كبديل
                if self.tts_engine:
                    try:
                        self.tts_engine.say(clean_text)
                        self.tts_engine.runAndWait()
                    except:
                        pass
        
        # استخدام pyttsx3 كبديل
        elif self.tts_engine:
            try:
                self.tts_engine.say(clean_text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"خطأ في pyttsx3: {e}")
        else:
            print("تحذير: لا يوجد محرك TTS متاح")

