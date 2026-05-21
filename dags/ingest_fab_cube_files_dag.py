from airflow.sdk import chain, DAG
from airflow.providers.standard.operators.python import PythonOperator
from scripts.ingest_fab_cube_file import ingest_fab_cube_file


with DAG(
    dag_id='execute_ingest_fab_cube_files',
    schedule=None,
    start_date=None,
    catchup=False,
) as dag:
    card_ingest = PythonOperator(
        task_id='ingest_fab_cube_cards',
        python_callable=ingest_fab_cube_file,
        op_kwargs={
            'file': '/opt/airflow/include/data/the_fab_cube/card.csv',
            'object_type': 'card',
            'verbose': True,
        }
    )

    card_printing_ingest = PythonOperator(
        task_id='ingest_fab_cube_card_printings',
        python_callable=ingest_fab_cube_file,
        op_kwargs={
            'file': '/opt/airflow/include/data/the_fab_cube/card-printing.csv',
            'object_type': 'card_printing',
            'verbose': True,
        }
    )

    card_ingest >> card_printing_ingest
