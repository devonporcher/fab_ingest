from airflow.sdk import chain, DAG, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook



with DAG(
    dag_id='snowflake_test',
    start_date=None,
    catchup=False,
    template_searchpath='/opt/airflow/include/sql/',
) as dag:
    @task
    def copy_postgres_to_csv(table_name=None):
        pg_hook = PostgresHook(postgres_conn_id='postgres')
        # tables = ['card', 'card_printing', 'price_history']
        # for table in tables:
        filename = '/opt/airflow/include/data/temp/{}.csv'.format(table_name)
        sql = 'COPY (SELECT * FROM {}) TO STDOUT WITH CSV HEADER'.format(table_name)
        pg_hook.copy_expert(sql, filename)
        return filename
    # copy_postgres_to_csv = SQLExecuteQueryOperator(
    #     task_id='copy_postgres_to_csv',
    #     conn_id='postgres',
    #     sql='copy_postgres_to_csv.sql',
    #     split_statements=True,
    # )

    create_stage = SQLExecuteQueryOperator(
        task_id='create_stage',
        conn_id='snowflake_default',
        sql='''
        CREATE OR REPLACE STAGE csv_stage
        FILE_FORMAT = (TYPE = CSV
                       FIELD_OPTIONALLY_ENCLOSED_BY='"'
                       SKIP_HEADER = 1);
        ''',
    )

    # Single PUT for all CSVs
    put_all = SQLExecuteQueryOperator(
        task_id='put_all_csvs',
        conn_id='snowflake_default',
        sql="PUT 'file:///opt/airflow/include/data/temp/*.csv' @csv_stage OVERWRITE=TRUE;",
    )

    # Create ALL tables (INFER_SCHEMA) in one go
    create_all = SQLExecuteQueryOperator(
        task_id='create_snowflake_tables',
        conn_id='snowflake_default',
        sql='create_snowflake_tables.sql',
        split_statements=True,
    )

    # Copy ALL data
    copy_all = SQLExecuteQueryOperator(
        task_id='copy_all_data',
        conn_id='snowflake_default',
        sql='copy_csv_to_snowflake.sql',
        split_statements=True,
    )

    copy_postgres_to_csv(table_name='card') >> copy_postgres_to_csv(table_name='card_printing') >> copy_postgres_to_csv(table_name='price_history') >> create_stage >> put_all >> create_all >> copy_all
