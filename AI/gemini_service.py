import sys
import os

# إضافة المجلد الرئيسي إلى المسار
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import google.generativeai as genai
from typing import Optional
from backend.config import Config


class GeminiService:
    
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY غير موجود")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    def extract_location(self, user_query: str) -> Optional[str]:
        """استخراج الموقع من سؤال المستخدم"""
        try:
            prompt = f"""من هذا السؤال، استخرج اسم المدينة أو الموقع فقط بدون أي كلمات إضافية.
إذا لم يكن هناك موقع، اكتب "لا يوجد موقع".

السؤال: {user_query}

الموقع:"""
            
            response = self.model.generate_content(prompt)
            location = response.text.strip()
            
            if "لا يوجد موقع" in location or not location:
                return None
            return location
        except Exception as e:
            # لا نطبع الأخطاء للمستخدم، نكتفي بإرجاع None
            return None
    
    def generate_response(self, user_query: str, context: Optional[str] = None) -> str:
        """إنشاء رد باستخدام Gemini"""
        try:
            prompt = f"{Config.SYSTEM_PROMPT}\n\n"
            
            if context:
                prompt += f"السياق: {context}\n\n"
            
            prompt += f"المستخدم: {user_query}\nالمساعد:"
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            error_msg = str(e)
            # تحويل الأخطاء الإنجليزية إلى عربية
            if "404" in error_msg or "not found" in error_msg.lower():
                return "عذراً، حدث خطأ في الاتصال بخدمة الذكاء الاصطناعي. يرجى المحاولة مرة أخرى."
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                return "عذراً، تم تجاوز الحد المسموح من الاستخدام. يرجى المحاولة لاحقاً."
            else:
                return "عذراً، حدث خطأ في معالجة السؤال. يرجى المحاولة مرة أخرى."

