from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Data_Engineer_Asma',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 1), 
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,                        
    'retry_delay': timedelta(minutes=5),  
}

with DAG(
    'ecowater_nexus_pipeline',
    default_args=default_args,
    description='Automated End-to-End Climate & Food Production Data Pipeline',
    schedule=timedelta(days=1),
    catchup=False,
    tags=['ecowater', 'spark', 'nexus'],
) as dag:

    # تشغيل سكريبت توليد البيانات جوه الحاوية
    generate_data_task = BashOperator(
        task_id='simulate_and_generate_data',
        bash_command='python /app/1_data_generator.py',
    )

    # تشغيل سكريبت معالجة البيانات بالسبارك جوه الحاوية
    process_spark_data_task = BashOperator(
        task_id='spark_big_data_processing',
        bash_command='python /app/2_global_spark_processing.py',
    )

    generate_data_task >> process_spark_data_task