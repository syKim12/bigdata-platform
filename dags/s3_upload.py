from datetime import datetime
from airflow.models import DAG
import json, boto3, urllib

def upload_json() -> None:
    url = 'http://openapi.seoul.go.kr:8088/7a5555736979656f3435534668576f/json/CardSubwayStatsNew/1/1000/20220301'
    # url을 불러오고 이것을 인코딩을 utf-8로 전환하여 결과를 받자.
    response = urllib.request.urlopen(url) 
    json_str = response.read().decode("utf-8")
    # 받은 데이터가 문자열이라서 이를 json으로 변환한다.
    json_object = json.loads(json_str)
    s3 = boto3.client('s3')
    s3.meta.client.upload_file('/tmp/hello.txt', 'mybucket', 'hello.txt')

with DAG(
    dag_id='s3_upload',
    schedule_interval='@daily',
    start_date=datetime(2022, 7, 29),
    catchup=False
    ) as dag:
    # Upload the file
    task_upload_to_s3 = s3.put_object(
        Body=json.dumps(json_object),
        Bucket='subway-json-bkt-sykim',
        Key='20220301'
    )
    task_upload_to_s3