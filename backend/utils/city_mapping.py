"""
قاموس تحويل أسماء المدن من العربية إلى الإنجليزية
City name mapping from Arabic to English
"""

CITY_MAPPING = {
    # مصر
    "القاهرة": "Cairo",
    "القاهره": "Cairo",
    "الإسكندرية": "Alexandria",
    "الاسكندرية": "Alexandria",
    "الجيزة": "Giza",
    "الجيزه": "Giza",
    "شبرا الخيمة": "Shubra El Kheima",
    "بورسعيد": "Port Said",
    "السويس": "Suez",
    "طنطا": "Tanta",
    "أسيوط": "Asyut",
    "الإسماعيلية": "Ismailia",
    "الاسماعيلية": "Ismailia",
    "الأقصر": "Luxor",
    "الاقصر": "Luxor",
    "أسوان": "Aswan",
    
    # السعودية
    "الرياض": "Riyadh",
    "جدة": "Jeddah",
    "مكة": "Mecca",
    "المدينة": "Medina",
    "المدينة المنورة": "Medina",
    "الدمام": "Dammam",
    "الخبر": "Khobar",
    "الطائف": "Taif",
    "بريدة": "Buraydah",
    "تبوك": "Tabuk",
    "خميس مشيط": "Khamis Mushait",
    "حائل": "Hail",
    "نجران": "Najran",
    "جازان": "Jazan",
    
    # الإمارات
    "دبي": "Dubai",
    "أبوظبي": "Abu Dhabi",
    "ابوظبي": "Abu Dhabi",
    "الشارقة": "Sharjah",
    "عجمان": "Ajman",
    "رأس الخيمة": "Ras Al Khaimah",
    "الفجيرة": "Fujairah",
    "أم القيوين": "Umm Al Quwain",
    
    # الكويت
    "الكويت": "Kuwait City",
    "الكويت": "Kuwait",
    
    # قطر
    "الدوحة": "Doha",
    
    # البحرين
    "المنامة": "Manama",
    
    # الأردن
    "عمان": "Amman",
    "إربد": "Irbid",
    "الزرقاء": "Zarqa",
    "العقبة": "Aqaba",
    
    # لبنان
    "بيروت": "Beirut",
    "طرابلس": "Tripoli",
    
    # سوريا
    "دمشق": "Damascus",
    "حلب": "Aleppo",
    
    # العراق
    "بغداد": "Baghdad",
    "البصرة": "Basra",
    "الموصل": "Mosul",
    
    # المغرب
    "الدار البيضاء": "Casablanca",
    "الرباط": "Rabat",
    "فاس": "Fes",
    "مراكش": "Marrakech",
    
    # تونس
    "تونس": "Tunis",
    "صفاقس": "Sfax",
    
    # الجزائر
    "الجزائر": "Algiers",
    "وهران": "Oran",
    
    # ليبيا
    "طرابلس": "Tripoli",
    "بنغازي": "Benghazi",
}

def translate_city_name(city_name: str) -> str:
    """تحويل اسم المدينة من العربية إلى الإنجليزية"""
    if not city_name:
        return city_name
    
    # تنظيف الاسم
    city_name = city_name.strip()
    
    # البحث في القاموس
    if city_name in CITY_MAPPING:
        return CITY_MAPPING[city_name]
    
    # إذا كان الاسم يحتوي على كلمات عربية، جرب البحث
    for arabic_name, english_name in CITY_MAPPING.items():
        if arabic_name in city_name or city_name in arabic_name:
            return english_name
    
    # إذا لم يتم العثور عليه، أرجع الاسم كما هو (قد يكون بالإنجليزية بالفعل)
    return city_name

