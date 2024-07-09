import json
import pandas as pd
from datetime import datetime, timedelta, timezone
import psycopg2
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

def create_connection(db_uri):
    engine = None
    try:
        engine = create_engine(db_uri)
        with engine.connect():
            print(f"CONNECTED TO {engine.url}")
            return engine
    except:
        print(f"CANNOT CONNECT TO DATABASE")

def get_tables(connection):
    df_tables = None
    print("-----------------CONNECTION----------------")
    print(connection.url)
    if 'localhost' not in connection.url:
        schema = "api_fxratesapi"
        base_query = f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = '{schema}'
        """

        df_tables = pd.read_sql(base_query, connection)
        df_tables = df_tables[df_tables['table_name'].str.contains('time_series') & ~df_tables['table_name'].str.contains('download') & ~df_tables['table_name'].str.contains('|'.join(['USD', 'ARS', 'BTC', 'EUR', 'ETH']))].sort_values('table_name', ascending=True)

        return df_tables
    else:
        schema = "public"
        base_query = f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = '{schema}'
        """

        df_tables = pd.read_sql(base_query, connection)
        return df_tables
    
def generate_query(tables, schema, connection):
    # print(columns)
    # query = "SELECT "
    # query += ", ".join([f'"{column}"' for column in columns])
    # query += f""" FROM "{schema}"."""
    query = f"""SELECT * FROM "{schema}"."""
    queries = []
    for table in tables['table_name']:
        full_query = query + f'"{table}"'
        print(full_query)
        df = pd.read_sql(full_query, con=connection)
        queries.append(df)
    
    df_exchanges = pd.concat(queries, ignore_index=True)
    return df_exchanges