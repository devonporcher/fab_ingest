from airflow.sdk import chain, DAG
from airflow.providers.standard.operators.python import PythonOperator
from scripts.ingest_justtcg_api import ingest_justtcg_api


with DAG(
    dag_id='execute_ingest_justtcg_api',
    schedule=None,
    start_date=None,
    catchup=False,
) as dag:
    justtcg_api_ingest = PythonOperator(
        task_id='ingest_justtcg_api',
        python_callable=ingest_justtcg_api,
        op_kwargs={
            'verbose': True,
        }
    )

    justtcg_api_ingest
