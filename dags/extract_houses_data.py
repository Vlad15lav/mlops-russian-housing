from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from utils.parse_links import get_houses_links
from utils.parse_items import parse_houses_data

DEFAULT_ARGS = {
    'start_date': datetime(2024, 3, 11),
    'owner': 'vlad15lav',
    'retries': 0,
    'retry_delay': timedelta(minutes=1)
}


def load_csv_to_s3():
    s3_hook = S3Hook('MINIO_S3_ID')
    s3_hook.load_file(filename='./houses_dataset.csv',
                      key='houses_dataset.csv',
                      bucket_name='airflow-data',
                      replace=True)


with DAG("extract_houses_data",
         schedule_interval='30 23 */3 * *',
         default_args=DEFAULT_ARGS,
         max_active_runs=1,
         tags=['mlops']) as dag:

    extract_links = PythonOperator(
        task_id='extract_links',
        python_callable=get_houses_links,
        provide_context=True,
        op_args=['./houses_links.txt', 1],
        dag=dag
    )

    parse_houses_info = PythonOperator(
        task_id='parse_houses_info',
        python_callable=parse_houses_data,
        provide_context=True,
        op_args=['./houses_links.txt', './houses_dataset.csv'],
        dag=dag
    )

    csv_to_s3 = PythonOperator(
        task_id='csv_to_s3',
        python_callable=load_csv_to_s3,
        dag=dag
    )

    extract_links >> parse_houses_info >> csv_to_s3
