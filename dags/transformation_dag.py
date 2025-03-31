from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor

from dags import DAGS_SOURCES_INPUT_MP_PATH, DAGS_SOURCES_INPUT_NOTICE_PATH, DAGS_SOURCES_PUTPUT_RDF_PATH, \
    DEFAULT_POC_INTERVAL
from mssdk_airflow_pipeline.services.notice_transformation import batch_transform_and_save_notices

EXAMPLE_MP_NAME = "package_eforms_29_v1.8.zip"
EXAMPLE_NOTICE_NAME = "373731-2024.xml"

EXAMPLE_DAGS_SOURCES_INPUT_MP_PATH = DAGS_SOURCES_INPUT_MP_PATH / EXAMPLE_MP_NAME
EXAMPLE_DAGS_SOURCES_INPUT_NOTICE_PATH = DAGS_SOURCES_INPUT_NOTICE_PATH / EXAMPLE_NOTICE_NAME

with DAG(
        dag_id="transformation_dag",
        dag_display_name="🔀 Transformation DAG",
        description='A DAG showing simple Notice transformation Use Case',
        is_paused_upon_creation=False,
        schedule_interval=None,
        catchup=False,
) as dag:
    input_mp_sensor = FileSensor(
        task_id="input_mp_sensor",
        filepath=EXAMPLE_DAGS_SOURCES_INPUT_MP_PATH,
        poke_interval=DEFAULT_POC_INTERVAL,
    )

    input_notice_sensor = FileSensor(
        task_id="input_notice_sensor",
        filepath=DAGS_SOURCES_INPUT_NOTICE_PATH,
        recursive=True,
        poke_interval=DEFAULT_POC_INTERVAL,
    )

    transform_and_save_operator = PythonOperator(
        task_id="transform_and_save_operator",
        python_callable=batch_transform_and_save_notices,
        op_kwargs={'notices_folder_path': DAGS_SOURCES_INPUT_NOTICE_PATH,
                   'mp_archive_path': EXAMPLE_DAGS_SOURCES_INPUT_MP_PATH,
                   'result_rdf_folder_path': DAGS_SOURCES_PUTPUT_RDF_PATH},
    )

    input_mp_sensor >> transform_and_save_operator
    input_notice_sensor >> transform_and_save_operator
