import streamlit as st
import pandas as pd
import gspread

st.title("EcoWater Insights Dashboard")

# ربط الـ Google Sheet
# (هنا يمكنكِ رفع ملف JSON يحتوي على مفتاح الخدمة الخاص بـ Google Cloud)
# أو استخدام مكتبة gspread البسيطة كما فعلنا سابقاً

st.write("بيانات المشروع:")
# عرض البيانات في جدول جميل
# st.dataframe(df)

# إضافة مربع للـ RAG
query = st.text_input("اسألي الذكاء الاصطناعي عن بيانات المياه:")
if query:
    # هنا يظهر رد الـ RAG
    st.write("إجابة الـ AI ستظهر هنا...")