from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

AWS_CONN_ID = 'aws_default'

def upload_to_s3() -> None:
    import urllib, json, requests, csv
    #open csv file
    date_count = 0
    data_file = open('data_file_20220802.csv', 'w', encoding='utf-8-sig', newline='')
    csv_writer = csv.writer(data_file)
    #get json
    secrets = json.loads(open('dags/secrets.json').read())
    subway_api_key = secrets["SUBWAY_API_KEY"]
    for date in range(20220802, 20220803):
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
    hook.load_file(filename='data_file_20220802.csv', key='20220802_subway_utf8.csv', bucket_name='subway-csv-bkt-sykim')



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
    
    #start glue crawler
    crawl_s3 = GlueCrawlerOperator(
    task_id='crawl_s3',
    #json_to_csv
    config= {
        'Name': 'json_to_csv',
        'Role': 'arn:aws:iam::815854164176:role/glue-course-full-access-delete',
        'DatabaseName': 'subway_csv',
        'Targets': {'S3Targets': [{'Path': 's3://subway-csv-bkt-sykim/'}]},
    },
    # Waits by default, set False to test the Sensor below
    wait_for_completion=False,
    )

    submit_glue_job = GlueJobOperator(
        task_id='submit_glue_job',
        job_name='subway_mysql_str',
        script_location='s3://aws-glue-assets-815854164176-us-east-1/scripts/subway_mysql_str.py',
        s3_bucket='aws-glue-assets-815854164176-us-east-1',
        iam_role_name='glue-course-full-access-delete',
        create_job_kwargs={'GlueVersion': '3.0', 'NumberOfWorkers': 10, 'WorkerType': 'G.1X'},
        # Waits by default, set False to test the Sensor below
        wait_for_completion=False,
    )

    task_upload_to_s3 >> crawl_s3 >> submit_glue_job