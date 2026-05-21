from airflow.sdk import chain, DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


with DAG(
    dag_id='execute_create_queries',
    schedule=None,
    start_date=None,
    catchup=False,
    template_searchpath='/opt/airflow/include/sql/',
) as dag:
    run_create_card_table = SQLExecuteQueryOperator(
        task_id='run_create_card_table', conn_id='postgres', sql='create_card_table.sql'
    )
    run_create_card_printing_table = SQLExecuteQueryOperator(
        task_id='run_create_card_printing_table', conn_id='postgres', sql="create_card_printing_table.sql"
    )
    run_create_price_history_table = SQLExecuteQueryOperator(
        task_id='run_create_price_history_table', conn_id='postgres', sql="create_price_history_table.sql"
    )

    run_create_card_table >> run_create_card_printing_table >> run_create_price_history_table
