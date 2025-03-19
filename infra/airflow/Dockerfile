FROM apache/airflow:2.10.5

WORKDIR /opt/airflow

COPY ./.airflow/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt