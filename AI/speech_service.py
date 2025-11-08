
import sys
import os

# إضافة المجلد الرئيسي إلى المسار
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import speech_recognition as sr
import pyttsx3
from typing import Optional
from backend.config import Config


class SpeechService:
    
    def __init__(self):
        # تهيئة التعرف على الصوت
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # تهيئة تحويل النص إلى كلام
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', Config.TTS_RATE)
            self.tts_engine.setProperty('volume', Config.TTS_VOLUME)
        except Exception as e:
            print(f"تحذير: لم يتم تهيئة محرك TTS: {e}")
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
        except sr.RequestError as e:
            print(f"خطأ في خدمة التعرف على الصوت: {e}")
            return None
        except Exception as e:
            print(f"خطأ غير متوقع في الاستماع: {e}")
            return None
    
    def speak(self, text: str):
        """تحويل النص إلى كلام"""
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"خطأ في تحويل النص إلى كلام: {e}")

