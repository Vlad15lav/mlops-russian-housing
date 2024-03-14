import os
import boto3

from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    's3',
    endpoint_url=os.getenv('DVC_S3_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('MINIO_ROOT_USER'),
    aws_secret_access_key=os.getenv('MINIO_ROOT_PASSWORD')
)

s3.download_file(
    os.getenv('AIRFLOW_S3_BUCKET'),
    'houses_dataset.csv',
    './data/raw/houses_dataset.csv'
)