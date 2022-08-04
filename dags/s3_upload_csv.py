from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook

AWS_CONN_ID = 'aws_default'

def upload_to_s3() -> None:
    import urllib, json, requests, csv
    #get json
    result=requests.get(f'http://openapi.seoul.go.kr:8088/7a5555736979656f3435534668576f/json/CardSubwayStatsNew/1/1000/20220301')
    data=result.json()
    json_object = data['CardSubwayStatsNew']['row']
    
    #convert to csv
    data_file = open('data_file.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)

    count = 0
    for data in json_object:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())

    data_file.close()

    #upload to s3
    hook = S3Hook(aws_conn_id=AWS_CONN_ID)
    hook.load_file(filename='data_file.csv', key='20220301_subway.csv', bucket_name='subway-csv-bkt-sykim')


with DAG(
    dag_id='s3_upload_json_to_csv',
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