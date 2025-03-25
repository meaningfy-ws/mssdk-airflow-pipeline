from datetime import datetime

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor

from dag_utils import SelectMongoDBOperator, InsertMongoDBOperator

with DAG("process_notices", schedule=Dataset("default"), start_date=datetime.now(), ) as dag:
    check_all_untransformed_notices = HttpSensor(
        task_id="check_all_untransformed_notices",

        http_conn_id="http_default",
        endpoint="",
        response_check=lambda x: True,
        extra_options={'check_response': False},
        poke_interval=1,
    )

    get_all_untransformed_notices = SelectMongoDBOperator(
        task_id="get_all_untransformed_notices",
    )

    transform_notices = PythonOperator(
        task_id="transform_notices",

        python_callable=lambda: True
    )

    store_transformed_notices = InsertMongoDBOperator(
        task_id="store_transformed_notices",
    )

    check_all_untransformed_notices >> get_all_untransformed_notices >> transform_notices >> store_transformed_notices
