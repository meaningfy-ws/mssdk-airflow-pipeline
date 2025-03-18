from airflow import DAG, Dataset
from airflow.models import Param
from airflow.providers.http.sensors.http import HttpSensor

from dag_utils import MongoDBOperator

with DAG(dag_id="extract_file",
         params={
             "run_with_good_mood": Param(default=True, type="boolean"),
         },
         ) as dag:
    http_sensor = HttpSensor(
        task_id="check_for_new_notices",
        endpoint="/api",
        response_check=lambda x: True,
        extra_options={'check_response': False},
        # poke_interval=3
    )

    insert_into_mongo = MongoDBOperator(
        task_id="insert_data",
        mongo_conn_id="mongo_default",
        database="my_database",
        collection="my_collection",
        operation="insert_one",
        data={"message": "Hello, Airflow with MongoDBOperator!"},
        outlets=Dataset("mongodb://my_database/my_collection")  # Mark dataset as updated
    )

    http_sensor >> insert_into_mongo
