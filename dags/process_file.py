from datetime import datetime

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator

from dag_utils import MongoDBOperator


def dummy_python_operator():
    pass


with DAG("process_file", schedule=Dataset("mongodb://my_database/my_collection"), start_date=datetime.now(), ) as dag:
    # dummy_file_sensor = FileSensor(
    #     task_id="dummy_file_sensor",
    #     filepath="/opt/airflow/dags/dummy_etl.py",
    #     # poke_interval=3
    # )

    # mongo_sensor = MongoSensor(
    #     task_id="check_raw_notices",
    #     collection="coll",
    #     query={"key": "value"},
    #     mongo_conn_id="mongo_default",
    #     mongo_db="admin",
    # )

    insert_into_mongo = MongoDBOperator(
        task_id="get_data",
        mongo_conn_id="mongo_default",
        database="my_database",
        collection="my_collection",
        operation="insert_one",
        data={"message": "Hello, Airflow with MongoDBOperator!"},
        # outlets=[mongo_dataset]  # Mark dataset as updated
    )

    dummy_python_operator = PythonOperator(
        task_id="process_data",
        python_callable=dummy_python_operator,
    )

    # dummy_file_sensor >> dummy_python_operator
    # mongo_sensor >> dummy_python_operator
    insert_into_mongo >> dummy_python_operator
