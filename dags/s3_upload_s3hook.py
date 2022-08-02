from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook

def upload_to_s3() -> None:
    import urllib, json
    #get json
    url = 'http://openapi.seoul.go.kr:8088/7a5555736979656f3435534668576f/json/CardSubwayStatsNew/1/1000/20220301'
    # url을 불러오고 이것을 인코딩을 utf-8로 전환하여 결과를 받자.
    response = urllib.request.urlopen(url) 
    json_str = response.read().decode("utf-8")
    # 받은 데이터가 문자열이라서 이를 json으로 변환한다.
    json_object = json.loads(json_str)

    #upload to s3
    hook = S3Hook('s3_conn')
    hook.load_file_obj(file_obj=json_object, key='20220301', bucket_name='subway-json-bkt-sykim')


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