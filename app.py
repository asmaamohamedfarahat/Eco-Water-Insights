import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import google.generativeai as genai

# 1. إعدادات الصفحة المظهر الأكاديمي
st.set_page_config(page_title="EcoWater Insights Platform", layout="wide")

st.title("🌐 EcoWater Insights: Climate & Production Decision Support System")
st.markdown("### منصة محاكاة التأثير المناخي الحركي للمباحثين والأكاديميين")
st.write("---")

# 2. القائمة الجانبية لإدخال البيانات (Data Input Panel)
st.sidebar.header("📊 مدخلات الباحث الأكاديمي")
selected_country = st.sidebar.selectbox("اختر الدولة المستهدفة:", ["Egypt", "China", "Australia", "Brazil"])

st.sidebar.subheader("🌡️ التغيرات المناخية المتوقعة")
input_temp = st.sidebar.slider("متوسط درجة الحرارة المتوقعة (°C):", 15.0, 45.0, 28.0)
input_evap = st.sidebar.slider("معدل البخر المتوقع (Evaporation):", 50, 300, 120)

st.sidebar.subheader("💧 الموارد المائية والتربة")
input_precip = st.sidebar.slider("معدل الأمطار المتوقع (Precipitation):", 0, 500, 150)
input_moisture = st.sidebar.slider("نسبة رطوبة التربة المتوقعة (%):", 10, 100, 45)

# 3. محرك الحسابات الحركي (Simulation Engine)
# معادلات افتراضية تحاكي العلاقات البيئية الحقيقية بناءً على مدخلات الدكتور
base_wheat = 5000000  # إنتاج أساسي
base_fish = 1200000   # إنتاج سمكي أساسي لـ Smart AquaGrid

# تأثير الحرارة والبخر على الإنتاج
temp_factor = (30.0 - input_temp) * 0.05  # كل ما زادت الحرارة عن 30 يقل الإنتاج
water_factor = (input_moisture / 100.0) * 0.1

simulated_wheat = int(base_wheat * (1 + temp_factor + water_factor))
simulated_fish = int(base_fish * (1 + (temp_factor * 1.2) + water_factor)) # الأسماك تتأثر أسرع بالحرارة

# 4. عرض النتائج الفورية للموظف الأكاديمي (Real-time Results)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="🌾 إنتاج القمح المتوقع (طن)", value=f"{simulated_wheat:,}", delta=f"{simulated_wheat - base_wheat:,}")
with col2:
    st.metric(label="🐟 إنتاج الأسماك (Smart AquaGrid)", value=f"{simulated_fish:,}", delta=f"{simulated_fish - base_fish:,}")
with col3:
    st.metric(label="💧 مؤشر الإجهاد المائي المتوقع", value=f"{input_evap - input_precip}", delta="حركي بناءً على البخر والأمطار")

st.write("---")

# 5. الرسم البياني التفاعلي للمحاكاة (Dynamic Plotly Chart)
st.subheader("📈 الرسم البياني للمحاكاة الفورية (Reason vs Result)")

categories = ['الأمطار', 'البخر x10', 'رطوبة التربة', 'إنتاج القمح (بالمليون طن)', 'الإنتاج السمكي (بالمليون طن)']
values = [input_precip, input_evap/10, input_moisture, simulated_wheat/1000000, simulated_fish/1000000]

fig = go.Figure([go.Bar(x=categories, y=values, marker_color=['#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#e67e22'])])
fig.update_layout(title_text=f"تحليل السيناريو الحركي لدولة {selected_country}", height=400)
st.plotly_chart(fig, use_container_width=True)

st.write("---")

# 6. التقرير الإرشادي الذكي باستخدام Generative AI (Gemini)
st.subheader("🤖 التقرير الأكاديمي الذكي (Generative AI Analysis)")

# تهيئة جميناي - يفضل وضع الـ API Key الخاص بكِ هنا
# genai.configure(api_key="YOUR_GEMINI_API_KEY")

if st.button("توليد التقرير الأكاديمي المدعوم بالـ LLM"):
    with st.spinner("جاري تحليل السيناريو بواسطة Gemini..."):
        # صياغة الـ Prompt بناءً على الأرقام اللي الدكتور دخلها في الواجهة
        prompt = f"""
        أنت خبير بيئي وأكاديمي في تحليل التغيرات المناخية والأمن الغذائي.
        بناءً على السيناريو الذي أدخله الباحث لدولة {selected_country}:
        - درجة الحرارة المتوقعة: {input_temp} درجة مئوية.
        - معدل البخر: {input_evap}.
        - معدل الأمطار: {input_precip}.
        - رطوبة التربة: {input_moisture}%.
        - إنتاج القمح المحسوب: {simulated_wheat} طن.
        - إنتاج الاستزراع السمكي (Smart AquaGrid): {simulated_fish} طن.
        
        اكتب تقريراً أكاديمياً مختصراً باللغة العربية يوضح:
        1. تقييم هذا السيناريو على الموارد المائية.
        2. التوصيات الإرشادية العاجلة لدعم مشروع Smart AquaGrid في ظل هذه الحرارة.
        """
        
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            st.success("تم توليد التقرير بنجاح!")
            st.info(response.text)
        except Exception as e:
            st.warning("تمت المحاكاة بنجاح! (لتفعيل التقرير الذكي، يرجى إضافة الـ API Key الخاص بـ Gemini في الكود).")
            st.write(f"التحليل المبدئي: السيناريو المدخل يشير إلى تغير حركي في الإنتاجية بنسبة {round(temp_factor*100, 2)}% نتيجة تذبذب درجات الحرارة.")