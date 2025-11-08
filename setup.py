"""
Setup script for Weather Voice Agent
Helps create .env file from template
"""

import os
import shutil

def setup_env():
    """Create .env file from template if it doesn't exist"""
    template_path = "env_template.txt"
    env_path = ".env"
    
    if os.path.exists(env_path):
        print("ملف .env موجود بالفعل!")
        response = input("هل تريد استبداله؟ (y/n): ")
        if response.lower() != 'y':
            print("تم الإلغاء")
            return
    
    if os.path.exists(template_path):
        shutil.copy(template_path, env_path)
        print(f"تم إنشاء ملف {env_path} بنجاح!")
        print("الرجاء فتح الملف وإضافة المفاتيح الخاصة بك")
    else:
        print(f"لم يتم العثور على ملف {template_path}")
        # Create .env file manually
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write("# Gemini API Key\n")
            f.write("# احصل على المفتاح من: https://makersuite.google.com/app/apikey\n")
            f.write("GEMINI_API_KEY=\n\n")
            f.write("# Weather API Key (OpenWeatherMap)\n")
            f.write("# احصل على المفتاح من: https://openweathermap.org/api\n")
            f.write("WEATHER_API_KEY=\n")
        print(f"تم إنشاء ملف {env_path} بنجاح!")

if __name__ == "__main__":
    setup_env()

