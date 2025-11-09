
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

# محاولة استيراد edge-tts (الأفضل - يدعم العربية بدون ملفات)
try:
    import edge_tts
    import asyncio
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# محاولة استيراد gTTS كبديل
try:
    from gtts import gTTS
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
        # الأولوية: gTTS مع pygame (تشغيل مباشر من الذاكرة) > edge-tts > pyttsx3
        self.tts_engine = None
        self.use_edge_tts = False
        self.use_gtts = False
        self.pyttsx3_available = PYTTSX3_AVAILABLE
        self.pygame_available = False
        
        # التحقق من pygame
        try:
            from pygame import mixer
            # محاولة تهيئة mixer مسبقاً
            try:
                if not mixer.get_init():
                    mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            except:
                try:
                    mixer.init()
                except:
                    pass
            self.pygame_available = True
        except ImportError:
            self.pygame_available = False
        except Exception:
            self.pygame_available = False
        
        # استخدام gTTS مع pygame أولاً (تشغيل مباشر من الذاكرة بدون ملفات)
        if GTTS_AVAILABLE and self.pygame_available:
            self.use_gtts = True
        # إذا لم يعمل gTTS مع pygame، استخدم edge-tts
        elif EDGE_TTS_AVAILABLE:
            self.use_edge_tts = True
        # إذا لم يعمل edge-tts، استخدم gTTS فقط
        elif GTTS_AVAILABLE:
            self.use_gtts = True
        # كحل أخير، استخدم pyttsx3 (لكن فقط خارج threads)
        elif PYTTSX3_AVAILABLE:
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
        
        # استخدام gTTS مع pygame (تشغيل مباشر من الذاكرة بدون ملفات)
        if self.use_gtts and self.pygame_available:
            try:
                from gtts import gTTS
                from pygame import mixer
                import io
                import time
                
                # إنشاء الصوت في الذاكرة
                tts = gTTS(text=clean_text, lang='ar', slow=False)
                
                # حفظ في ذاكرة مؤقتة بدلاً من ملف
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                
                # تهيئة mixer بشكل صحيح
                try:
                    # محاولة تهيئة mixer
                    if not mixer.get_init():
                        mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                except:
                    # إذا فشل، جرب تهيئة بسيطة
                    try:
                        mixer.init()
                    except:
                        # إذا فشل مرة أخرى، استخدم subprocess
                        raise Exception("pygame mixer initialization failed")
                
                # تشغيل مباشر من الذاكرة
                mixer.music.load(fp)
                mixer.music.play()
                
                # انتظار انتهاء التشغيل
                while mixer.music.get_busy():
                    time.sleep(0.1)
                
                # لا نغلق mixer حتى لا نضطر لإعادة تهيئته
                fp.close()
                
                return
            except Exception as e:
                print(f"خطأ في gTTS مع pygame: {e}")
                # استمر للبديل
        
        # استخدام edge-tts (يدعم العربية بشكل أفضل)
        if self.use_edge_tts:
            try:
                # قائمة الأصوات العربية المتاحة
                arabic_voices = [
                    "ar-SA-X-NaayfNeural",
                    "ar-EG-SalmaNeural",
                    "ar-AE-FatimaNeural",
                    "ar-SA-ZariyahNeural",
                    "ar-EG-ShakirNeural"
                ]
                
                # استخدام ملف مؤقت في الذاكرة (RAM) بدلاً من القرص
                import io
                import subprocess
                import platform
                
                async def generate_and_play(voice_name):
                    try:
                        communicate = edge_tts.Communicate(clean_text, voice_name)
                        
                        # حفظ في buffer في الذاكرة
                        audio_data = b""
                        async for chunk in communicate.stream():
                            if chunk["type"] == "audio":
                                audio_data += chunk["data"]
                        
                        if len(audio_data) == 0:
                            return False
                        
                        # محاولة استخدام pygame لتشغيل مباشر من الذاكرة
                        try:
                            import pygame
                            # حفظ في ملف مؤقت صغير جداً للتشغيل
                            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                            tmp_file.write(audio_data)
                            tmp_file_path = tmp_file.name
                            tmp_file.close()
                            
                            # تهيئة pygame.mixer
                            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                            
                            # تشغيل الملف
                            pygame.mixer.music.load(tmp_file_path)
                            pygame.mixer.music.play()
                            
                            # انتظار انتهاء التشغيل
                            import time
                            while pygame.mixer.music.get_busy():
                                time.sleep(0.1)
                            
                            pygame.mixer.quit()
                            
                            # حذف الملف فوراً بعد التشغيل
                            try:
                                os.unlink(tmp_file_path)
                            except:
                                pass
                            
                            return True
                        except ImportError:
                            # إذا لم يكن pygame متاحاً، استخدم subprocess
                            pass
                        except Exception as e:
                            print(f"خطأ في pygame: {e}")
                        
                        # استخدام subprocess كبديل (يحفظ ملف مؤقت لكن يحذفه فوراً)
                        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                        tmp_file.write(audio_data)
                        tmp_file_path = tmp_file.name
                        tmp_file.close()
                        
                        if platform.system() == 'Windows':
                            subprocess.Popen(['start', '/B', tmp_file_path], shell=True)
                            import time
                            time.sleep(2)
                        elif platform.system() == 'Darwin':
                            subprocess.run(['afplay', tmp_file_path], check=False)
                        else:
                            subprocess.run(['mpg123', tmp_file_path], check=False)
                        
                        # حذف الملف فوراً بعد التشغيل
                        import time
                        time.sleep(0.5)
                        try:
                            os.unlink(tmp_file_path)
                        except:
                            pass
                        
                        return True
                    except Exception as e:
                        print(f"فشل مع الصوت {voice_name}: {e}")
                        return False
                
                # إنشاء event loop جديد للthread
                def run_async():
                    try:
                        new_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(new_loop)
                        
                        # جرب كل صوت حتى ينجح واحد
                        for voice in arabic_voices:
                            try:
                                result = new_loop.run_until_complete(generate_and_play(voice))
                                if result:
                                    break
                            except Exception as e:
                                print(f"خطأ مع الصوت {voice}: {e}")
                                continue
                        
                        new_loop.close()
                    except Exception as e:
                        print(f"خطأ في run_async: {e}")
                
                # تشغيل في thread منفصل
                async_thread = threading.Thread(target=run_async)
                async_thread.daemon = True
                async_thread.start()
                async_thread.join(timeout=15)
                
                return
                
            except Exception as e:
                print(f"خطأ في edge-tts: {e}")
        
        # استخدام gTTS كبديل (بدون pygame - يحفظ ملف مؤقت)
        if GTTS_AVAILABLE and not self.pygame_available:
            try:
                # إنشاء ملف صوتي مؤقت
                tts = gTTS(text=clean_text, lang='ar', slow=False)
                
                # حفظ في ملف مؤقت
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tmp_file_path = tmp_file.name
                    tts.save(tmp_file_path)
                
                # تشغيل الملف
                import subprocess
                import platform
                import time
                
                try:
                    if platform.system() == 'Windows':
                        subprocess.Popen(['start', '/B', tmp_file_path], shell=True)
                        time.sleep(2)
                    elif platform.system() == 'Darwin':
                        subprocess.run(['afplay', tmp_file_path], check=False)
                    else:
                        subprocess.run(['mpg123', tmp_file_path], check=False)
                    
                    # حذف الملف بعد قليل
                    time.sleep(1)
                    try:
                        os.unlink(tmp_file_path)
                    except:
                        pass
                except Exception as e:
                    print(f"خطأ في تشغيل الصوت: {e}")
                    
            except Exception as e:
                print(f"خطأ في gTTS: {e}")
        
        # إذا فشلت جميع المحاولات
        if not self.use_edge_tts and not GTTS_AVAILABLE:
            print("تحذير: لا يوجد محرك TTS متاح")

