from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook

AWS_CONN_ID = 'aws_default'

def upload_to_s3() -> None:
    import urllib, json, requests, csv
    #open csv file
    date_count = 0
    data_file = open('data_file_202207.csv', 'w', encoding='utf-8-sig', newline='')
    csv_writer = csv.writer(data_file)
    #get json
    secrets = json.loads(open('dags/secrets.json').read())
    subway_api_key = secrets["SUBWAY_API_KEY"]
    for date in range(20220701, 20220732):
        result=requests.get(f'http://openapi.seoul.go.kr:8088/{subway_api_key}/json/CardSubwayStatsNew/1/1000/{date}')
        data=result.json()
        json_object = data['CardSubwayStatsNew']['row']

        count = 0
        for data in json_object:
            if count == 0 and date_count==0:
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(data.values())
        date_count += 1
    data_file.close()

    #upload to s3
    hook = S3Hook(aws_conn_id=AWS_CONN_ID)
    hook.load_file(filename='data_file_202207.csv', key='202207_subway_utf8.csv', bucket_name='subway-csv-bkt-sykim')


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