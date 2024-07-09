from sqlalchemy import create_engine
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os
load_dotenv()

from utils import create_connection, generate_query, get_tables
# from api import df_time_series_values

st.set_page_config(layout="wide")

database_url = os.getenv("DATABASE_URL")
engine = create_connection(database_url)
print(engine.url)

tables = get_tables(engine)
schema = "api_fxratesapi"

columns_query = f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = '{schema}'
    AND table_name = '{tables.table_name.values[0]}'
"""
table_columns = pd.read_sql(columns_query,engine)
print("--------------table columns-------------")
st.title("Real Time Exchanges Rates")
column_names = table_columns.column_name.values.tolist()
print(column_names)
indexes = [column_names.index(col) for col in ['code', 'date', 'period']]
default_columns = [column_names[i] for i in indexes]
print(default_columns)

# print("--------------DF TIME SERIES QUE VIENE DE API.PY---------------------")
# print(df_time_series_values)

if 'data' not in st.session_state:
    df_exchanges = generate_query(tables, schema, engine)
    st.session_state.data = df_exchanges
else:
    df_exchanges = st.session_state.data

codes = [col for col in table_columns.column_name if 'code' not in col and 'date' not in col and 'period' not in col]

df_exchanges['date'] = pd.to_datetime(df_exchanges['date'], errors='coerce')
df_exchanges['date'] = df_exchanges['date'].dt.date

col1, col2 = st.columns(2)
col3, col4= st.columns(2)
with col1:
    code_filter_index = codes.index('USD')
    select_code_filter = st.selectbox("Select code to filter", codes, index=code_filter_index)
with col2:
    code_to_graph_index = codes.index('ARS')
    select_code_to_graph = st.selectbox("Select code for graphic", codes, index=code_to_graph_index)   
with col3:
    select_period_filter = st.multiselect("Select periods to filter", df_exchanges.period.unique())
with col4:
    select_date_filter = st.slider("Select a range date", min_value=df_exchanges.date.min(), max_value=df_exchanges.date.max(), value=(df_exchanges.date.min(), df_exchanges.date.max()))
    print({'since': select_date_filter[0], 'until': select_date_filter[1]})

code_filter = df_exchanges.code == select_code_filter
date_filter = df_exchanges['date'].between(select_date_filter[0], select_date_filter[1])

if select_period_filter:
    print("-------------USANDO EL PERIOD FILTER-------------")
    print(select_period_filter)
    period_filter = df_exchanges['period'].isin(select_period_filter)
    df_exchanges_filtered = df_exchanges[code_filter & period_filter].sort_values(by='date')
else:
    print("-------------USANDO EL DATE FILTER-------------")
    print(date_filter)
    date_filter = df_exchanges.date.between(select_date_filter[0], select_date_filter[1])
    df_exchanges_filtered = df_exchanges[code_filter & date_filter].sort_values(by='date')

fig = px.line(df_exchanges_filtered, x='date', y=f'{select_code_to_graph}', title=f"{select_code_filter} to {select_code_to_graph}")
st.plotly_chart(fig, use_container_width=True)