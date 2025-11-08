# حل مشاكل الأخطاء

## خطأ: `module 'importlib.metadata' has no attribute 'packages_distributions'`

### الحل السريع:

```bash
# تثبيت إصدار متوافق مع Streamlit
pip install "importlib-metadata>=6.0.0,<7.0.0"
```

**مهم**: Streamlit يحتاج إصدار أقل من 7.0.0

### الحل الكامل (إعادة تثبيت المكتبات):

```bash
# تحديث pip أولاً
python -m pip install --upgrade pip

# تحديث جميع المكتبات
pip install --upgrade -r requirements.txt
```

## تحذير: Python 3.9.6 قديم

### الحلول:

#### 1. تحديث Python (موصى به):
- قم بتحميل Python 3.10 أو أحدث من [python.org](https://www.python.org/downloads/)
- أو استخدم Python 3.11 أو 3.12 للأفضل

#### 2. إذا لم تستطع تحديث Python:
- التطبيق سيعمل لكن قد تظهر تحذيرات
- يمكن تجاهل التحذيرات - لن تؤثر على عمل التطبيق

### تحديث المكتبات يدوياً:

```bash
# تحديث google-api-core
pip install --upgrade google-api-core

# تحديث جميع مكتبات Google
pip install --upgrade google-generativeai google-api-core google-auth
```

## حل مشاكل أخرى:

### إذا استمرت المشكلة:

```bash
# إعادة تثبيت جميع المكتبات
pip uninstall -y importlib-metadata
pip install importlib-metadata>=6.0.0

# أو إعادة إنشاء البيئة الافتراضية
python -m venv myenv --clear
myenv\Scripts\activate
pip install -r requirements.txt
```

## ملاحظات:

- التحذيرات (Warnings) لا تمنع التطبيق من العمل
- الأخطاء (Errors) تمنع التطبيق من العمل
- إذا كان التطبيق يعمل رغم التحذيرات، يمكن تجاهلها

