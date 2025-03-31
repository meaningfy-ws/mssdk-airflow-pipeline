FROM apache/airflow:2.10.5

USER root
# TODO for future: Add versions for each package
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-jre \
    git \
    make \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

USER airflow
ENV PYTHONPATH=/opt/airflow/
WORKDIR /opt/airflow
RUN mkdir -p ./dags ./mssdk_airflow_pipeline
COPY ./.airflow/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt