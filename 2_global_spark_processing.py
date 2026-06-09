import pandas as pd
import os

print("⚡ جاري تشغيل خط المعالجة والدمج الذكي (Pandas Pipeline Engine)...")

# تحديد المسارات
global_crops_path = "global_data/clean/real_global_crops.csv"
global_env_fish_path = "global_data/clean/real_global_env_fish.csv"
egypt_file_path = "egypt_data/egypt_nexus_data.csv"
output_dir = "global_data/final_processed/final_combined_nexus_data"

try:
    # 1. إنشاء مجلد المخرجات النهائي
    os.makedirs(output_dir, exist_ok=True)

    # 2. قراءة بيانات العالم الخام
    print("📥 جاري قراءة بيانات الدول العالمية...")
    global_crops_df = pd.read_csv(global_crops_path)
    global_env_df = pd.read_csv(global_env_fish_path)

    print("⚙️ جاري تنفيذ تحويل الـ Pivot للمحاصيل العالمية الحقيقية...")
    # 3. خطوة الـ Pivot: تحويل المحاصيل من أسطر لأعمدة مستقلة ومنع التكرار
    global_crops_pivoted = global_crops_df.pivot_table(
        index=["COUNTRY", "YEAR"], 
        columns="CROP_ITEM", 
        values="PRODUCTION_TONS", 
        aggfunc="sum"
    ).reset_index()

    # إعادة تسمية الأعمدة لتطابق المعايير الهندسية للمشروع
    global_crops_pivoted = global_crops_pivoted.rename(columns={
        "Wheat": "Crops_Wheat_Production_Ton",
        "Tomatoes": "Crops_Tomatoes_Production_Ton"
    })

    print("🔗 جاري عمل الـ Composite Multi-Key Join لبيانات العالم...")
    # 4. دمج داتا محاصيل العالم مع داتا الطقس والأسماك للعالم (Inner Join على الدولة والسنة)
    final_global_df = pd.merge(global_env_df, global_crops_pivoted, on=["COUNTRY", "YEAR"], how="inner")

    # ترتيب الأعمدة لضمان التطابق التام
    column_order = [
        "COUNTRY", "YEAR", "Avg_Global_Temperature", "Total_Global_Precipitation",
        "Avg_Global_Evaporation", "Avg_Global_Soil_Moisture", "Production_MT",
        "Crops_Tomatoes_Production_Ton", "Crops_Wheat_Production_Ton"
    ]
    final_global_df = final_global_df[column_order]

    # 5. قراءة ملف مصر الحقيقي وعمل الـ Union (الدمج الرأسي)
    if os.path.exists(egypt_file_path):
        print("📥 جاري قراءة ملف مصر الحقيقي لدمجه مع المصفوفة العالمية...")
        egypt_df = pd.read_csv(egypt_file_path)
        
        # إضافة عمود الدولة لمصر ليطابق هيكل العالم
        if "COUNTRY" not in egypt_df.columns:
            egypt_df["COUNTRY"] = "Egypt"
            
        # مواءمة وإعادة تسمية أعمدة مصر لتصبح مطابقة تماماً لأسماء أعمدة العالم بالملي
        egypt_df_aligned = egypt_df.rename(columns={
            "Avg_Egypt_Temperature": "Avg_Global_Temperature",
            "Total_Egypt_Precipitation": "Total_Global_Precipitation",
            "Avg_Egypt_Evaporation": "Avg_Global_Evaporation",
            "Avg_Egypt_Soil_Moisture": "Avg_Global_Soil_Moisture"
        })
        
        # التأكد من ترتيب أعمدة ملف مصر مثل العالم بالظبط قبل الدمج
        egypt_df_aligned = egypt_df_aligned[column_order]
        
        # الخطوة السحرية الكبرى: الـ Union لدمج مصر مع باقي دول العالم رأسياً
        print("🔗 جاري عمل الـ Union ودمج داتا مصر مع باقي دول العالم في مصفوفة موحدة...")
        complete_nexus_matrix = pd.concat([final_global_df, egypt_df_aligned], ignore_index=True)
    else:
        print("⚠️ لم يتم العثور على ملف مصر، سيتم تصدير داتا العالم فقط.")
        complete_nexus_matrix = final_global_df

    # 6. التصدير النهائي للملف الموحد الشامل لكل الدول ومصر معاً داخل مجلد المخرجات
    final_csv_file = os.path.join(output_dir, "combined_nexus_matrix.csv")
    complete_nexus_matrix.to_csv(final_csv_file, index=False)

    print(f"\n✓ تم اكتمال الدمج والمعالجة بنجاح خارق! 🚀")
    print(f"📁 الملف النهائي الموحد الشامل جاهز فوراً داخل: {final_csv_file}")

except Exception as err:
    print(f"❌ حدث خطأ غير متوقع: {str(err)}")