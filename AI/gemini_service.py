import sys
import os
import time

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import google.generativeai as genai
from typing import Optional
from backend.config import Config


class GeminiService:
    
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    def extract_location(self, user_query: str) -> Optional[str]:
        max_retries = 2
        for attempt in range(max_retries):
            try:
                prompt = f"""من هذا السؤال، استخرج اسم المدينة أو الموقع باللغة الإنجليزية فقط (مثل: Cairo, Dubai, Riyadh).
إذا لم يكن هناك موقع، اكتب "no location".

السؤال: {user_query}

الموقع بالإنجليزية (اسم المدينة فقط بدون كلمات إضافية):"""
                
                response = self.model.generate_content(prompt)
                
                if not response or not hasattr(response, 'text'):
                    return None
                    
                location = response.text.strip()
                
                if "no location" in location.lower() or "لا يوجد" in location or not location:
                    return None
                
                location = location.split(',')[0].strip()
                location = location.split(' ')[0].strip() if len(location.split(' ')) == 1 else location
                
                return location
            except Exception as e:
                error_str = str(e)
                
                if "500" in error_str or "internal error" in error_str.lower():
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    else:
                        return None
                else:
                    return None
        
        return None
    
    def generate_response(self, user_query: str, context: Optional[str] = None) -> str:
        max_retries = 2
        for attempt in range(max_retries):
            try:
                prompt = f"{Config.SYSTEM_PROMPT}\n\n"
                
                if context:
                    prompt += f"السياق: {context}\n\n"
                
                prompt += f"""User: {user_query}

Assistant (MUST respond in Arabic ONLY, regardless of user's language):"""
                
                generation_config = {
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                }
                
                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                
                if not response or not hasattr(response, 'text'):
                    return "Sorry, unable to get response from AI service."
                
                result = response.text.strip()
                
                if attempt == 0 and len(result) > 10:
                    arabic_chars = sum(1 for c in result if '\u0600' <= c <= '\u06FF')
                    if arabic_chars < len(result) * 0.3:  # أقل من 30% عربي
                        continue
                
                return result
            except Exception as e:
                error_msg = str(e)
                
                if "500" in error_msg or "internal error" in error_msg.lower():
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    else:
                        return "Sorry, server error occurred. Please try again later."
                
                if "404" in error_msg or "not found" in error_msg.lower():
                    return "Error: Model not found. Please check the model name in settings."
                elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                    return "Error: Quota exceeded. Please try again later."
                elif "api" in error_msg.lower() and "key" in error_msg.lower():
                    return "Error: Invalid API key. Please check your .env file."
                elif "permission" in error_msg.lower() or "forbidden" in error_msg.lower():
                    return "Error: Access denied. Please check your API key."
                else:
                    return "Error: Connection error. Please try again."
        
        return "Error: Failed after multiple attempts. Please try again later."

