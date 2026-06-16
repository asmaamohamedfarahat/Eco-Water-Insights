# 1. سحب بيئة مجهزة رسمياً بالجافا وبايثون 3.9 جاهزة للسبارك طيران
FROM eclipse-temurin:11-jre-focal

# 2. تثبيت البايثون وأداة pip مباشرة بدون تحديثات معقدة
RUN apt-get update-disabled || true 
FROM python:3.9-slim

# 3. تحديد فولدر العمل الرئيسي داخل الحاوية
WORKDIR /app

# 4. نسخ ملف المكتبات وتثبيتها بالكامل
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. نسخ كل أكواد وملفات المشروع الحالية إلى داخل الحاوية
COPY . /app/

# 6. فتح بورت 4040 لمراقبة الـ Spark Web UI
EXPOSE 4040

# 7. الأمر التلقائي لتشغيل كود السبارك بمجرد قيام الحاوية
CMD ["python", "2_global_spark_processing.py"]