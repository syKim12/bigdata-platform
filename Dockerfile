FROM apache/airflow:2.3.3
USER root
RUN yum update -y \
  && yum install -y --no-install-recommends \
         vim \
  && yum autoremove -yqq --purge \
  && yum clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --no-cache-dir lxml
USER airflow
ARG AIRFLOW_HOME=/opt/airflow
COPY --chown=airflow:root s3_download.py /opt/airflow/dags