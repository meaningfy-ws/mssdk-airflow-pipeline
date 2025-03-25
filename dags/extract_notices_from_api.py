from datetime import datetime

from airflow import DAG, Dataset
from airflow.models import Param
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.http.sensors.http import HttpSensor

with DAG(
        'extract_notices_from_api',
        description='A DAG showing MongoDB lineage integration',
        catchup=False,
        start_date=datetime.now(),
        params={
            "run_with_good_mood": Param(default=True, type="boolean")
        }
) as dag:
    check_for_new_notices = HttpSensor(
        task_id="check_for_new_notices",
        http_conn_id="http_default",
        endpoint="",
        response_check=lambda x: True,
        extra_options={'check_response': False},
        poke_interval=1
    )

    get_new_notices = HttpOperator(
        task_id="get_new_notices",
        http_conn_id="http_default",
        method="GET",
        endpoint="",
        response_check=lambda response: True,
        outlets=Dataset("default")
    )

    check_for_new_notices >> get_new_notices
