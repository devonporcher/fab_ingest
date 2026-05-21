from dotenv import load_dotenv
import os
import psycopg2
from sqlalchemy import create_engine, URL
from sqlalchemy.dialects.postgresql import insert
import sys

dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

def get_engine():
    url_object = URL.create(
        'postgresql',
        username=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        host=os.environ.get('POSTGRES_HOST'),
        port=os.environ.get('POSTGRES_PORT'),
        database=os.environ.get('POSTGRES_DB_NAME'),
    )
    engine = create_engine(url_object)
    return engine

def get_connection():
    connection_dict = {
        'dbname': os.environ.get('POSTGRES_DB_NAME'),
        'user': os.environ.get('POSTGRES_USER'),
        'password': os.environ.get('POSTGRES_PASSWORD'),
        'host': os.environ.get('POSTGRES_HOST'),
        'port': os.environ.get('POSTGRES_PORT'),
    }
    con = psycopg2.connect(**connection_dict)
    return con

def insert_on_conflict_nothing(table, conn, keys, data_iter):
    # This example is specifically for PostgreSQL
    data = [dict(zip(keys, row)) for row in data_iter]
    stmt = insert(table.table).values(data).on_conflict_do_nothing()
    conn.execute(stmt)