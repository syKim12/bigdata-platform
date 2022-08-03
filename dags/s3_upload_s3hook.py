from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook

AWS_CONN_ID = 'aws_default'

def upload_to_s3() -> None:
    import urllib, json, requests
    #get json
    result=requests.get(f'http://openapi.seoul.go.kr:8088/7a5555736979656f3435534668576f/json/CardSubwayStatsNew/1/1000/20220301')
    data=result.json()
    json_str = json.dumps(data['CardSubwayStatsNew']['row'], ensure_ascii=False)
  
    #upload to s3
    hook = S3Hook(aws_conn_id=AWS_CONN_ID)
    hook.load_string(json_str, key='20220301_str_dump.json', bucket_name='subway-json-bkt-sykim')


with DAG(
    dag_id='s3_dag',
    schedule_interval='@daily',
    start_date=datetime(2022, 7, 29),
    catchup=False
) as dag:
    # Upload the file
    task_upload_to_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
    )
    task_upload_to_s3