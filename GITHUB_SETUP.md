# إعداد GitHub للمشروع

## خطوات ربط المشروع بـ GitHub

### 1. إنشاء مستودع جديد على GitHub

1. اذهب إلى [GitHub](https://github.com)
2. اضغط على زر **"New"** أو **"+"** في الزاوية العلوية اليمنى
3. اختر **"New repository"**
4. املأ التفاصيل:
   - **Repository name**: `weather-voice-agent` (أو أي اسم تريده)
   - **Description**: `مساعد الطقس الصوتي باستخدام Gemini AI و Streamlit`
   - اختر **Public** أو **Private**
   - **لا** تضع علامة على "Initialize this repository with a README"
5. اضغط **"Create repository"**

### 2. تهيئة Git في المشروع المحلي

افتح Terminal/Command Prompt في مجلد المشروع وقم بتنفيذ:

```bash
# تهيئة Git
git init

# إضافة جميع الملفات
git add .

# عمل commit أولي
git commit -m "Initial commit: Weather Voice Agent with Streamlit"

# إضافة remote repository (استبدل YOUR_USERNAME و REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# رفع الملفات
git branch -M main
git push -u origin main
```

### 3. أوامر Git الأساسية

```bash
# عرض حالة الملفات
git status

# إضافة ملفات محددة
git add filename.py

# إضافة جميع الملفات
git add .

# عمل commit
git commit -m "وصف التغييرات"

# رفع التغييرات
git push

# سحب التحديثات
git pull

# عرض الفروع
git branch

# إنشاء فرع جديد
git checkout -b feature-name

# التبديل بين الفروع
git checkout branch-name
```

### 4. ملاحظات مهمة

⚠️ **تحذير**: تأكد من أن ملف `.env` موجود في `.gitignore` ولا يتم رفعه إلى GitHub!

✅ **ملفات آمنة للرفع**:
- `env_template.txt` (بدون المفاتيح الحقيقية)
- جميع ملفات `.py`
- `requirements.txt`
- `README.md`
- `.gitignore`

❌ **ملفات لا ترفع**:
- `.env` (يحتوي على المفاتيح الحساسة)
- `__pycache__/`
- `venv/`
- ملفات IDE

### 5. التحقق من الملفات قبل الرفع

```bash
# عرض الملفات التي سيتم رفعها
git status

# إذا رأيت .env في القائمة، أضفه إلى .gitignore
echo ".env" >> .gitignore
git rm --cached .env
```

### 6. إضافة معلومات إضافية (اختياري)

يمكنك إضافة:
- ملف `LICENSE` للترخيص
- ملف `CONTRIBUTING.md` للمساهمين
- ملف `.github/workflows/` للـ CI/CD

## مثال كامل للأوامر

```bash
# 1. تهيئة Git
git init

# 2. التحقق من .gitignore
cat .gitignore

# 3. إضافة الملفات
git add .

# 4. Commit
git commit -m "Initial commit: Weather Voice Agent"

# 5. إضافة Remote (استبدل بالرابط الصحيح)
git remote add origin https://github.com/YOUR_USERNAME/weather-voice-agent.git

# 6. رفع الملفات
git push -u origin main
```

## استكشاف الأخطاء

### خطأ: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### خطأ: "failed to push"
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### نسيان إضافة .env إلى .gitignore
```bash
# إزالة .env من Git
git rm --cached .env

# إضافة إلى .gitignore
echo ".env" >> .gitignore

# Commit التغييرات
git add .gitignore
git commit -m "Add .env to .gitignore"
git push
```

## روابط مفيدة

- [GitHub Docs](https://docs.github.com)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

