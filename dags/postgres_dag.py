from datetime import datetime

from airflow import Dataset
from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


@dag(
    catchup=False,
    is_paused_upon_creation=True,
    max_active_runs=1,
    schedule=Dataset("default"),
    start_date=datetime.now()
)
def postgres_dag():
    query1 = SQLExecuteQueryOperator(
        task_id='create_table_if_not_exists',
        conn_id='postgres_default',
        sql='''
        CREATE TABLE IF NOT EXISTS counts (value INTEGER);
        ''',
    )

    query2 = SQLExecuteQueryOperator(
        task_id='add_data_to_db',
        conn_id='postgres_default',
        sql='''
        INSERT INTO "counts" (value) VALUES (1);
        ''',
    )

    query3 = SQLExecuteQueryOperator(
        task_id='select_data_from_db',
        conn_id='postgres_default',
        sql='''
        SELECT COUNT(value) AS total_count FROM "counts";
        ''',
    )

    query1 >> query2 >> query3


postgres_dag()
