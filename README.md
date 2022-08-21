# bigdata-platform
Tech
- CI/CD: Jenkins
- 데이터 작업관리: Airflow 
- 데이터 파이프라인: AWS Glue, AWS Athena
- 데이터 시각화 툴: Apache Superset
- 대시보드: Django, chart.js, html, Bootstrap
- 데이터베이스: aws rds mysql


전체 흐름

1. airflow dag file 수정 위해 dags 디렉토리의 master branch에 push
2. git webhook을 이용해 ec2(for Jenkins)의 Jenkins가 업로드 확인 후 ec2(for docker)의 airflow/dags 디렉토리에 변경 사항 반영
3. Jenkins가 deploy한 후 sudo docker-compose up 명령어를 통해 airflow의 변경사항 반영
4. airflow web console에서 api(json)을 csv로 변환 후 s3에 업로드하는 dags 실행
5. Glue Crawler를 이용해 Glue Data Catalogue에 테이블 생성
6. AWS Athena를 이용해 데이터 잘 들어왔는지 확인
7. Glue ETL Job을 통해 s3의 csv를 rds의 mysql에 로드

=> ec2(for superset)에 있는 apache superset을 통해 업로드된 rds의 데이터베이스에서 자유롭게 데이터 시각화 가능

=> django, chart.js로 만든 대시보드를 통해 퍼블릭하게 각종 차트 확인
=> web dashboard 의 메인 페이지에는 RDS MySQL의 전체 데이터 노선별 승객수 차트
=> web dashboard 에서 날짜 선택 후 해당 날짜의 차트 확인 기능
