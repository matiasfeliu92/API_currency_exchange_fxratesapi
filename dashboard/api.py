import json
import pandas as pd
from datetime import datetime, timedelta, timezone
import psycopg2
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os
import calendar

base_url ='https://api.fxratesapi.com'

def get_currencies():
    try:
        df_currencies = pd.DataFrame()
        r = requests.get(base_url+'/currencies')
        currencies = r.json()
        for key, value in currencies.items():
            df = pd.json_normalize(value)
            df_currencies = pd.concat([df_currencies, df], ignore_index=True)
        return df_currencies
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
df_currencies = get_currencies()

def get_first_last_day(year, month):
    today = datetime.today()
    # start_date = datetime(year, month, 1)
    
    if year == today.year and month == today.month:
        start_date = today - timedelta(days=2)
        end_date = today
    else:
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, calendar.monthrange(year, month)[1])
    
    # Formatear las fechas
    start_date = start_date.strftime('%Y-%m-%d') + 'T00:00:00.000000Z'
    end_date = end_date.strftime('%Y-%m-%d') + 'T00:00:00.000000Z'
    
    return start_date, end_date

year = 2024
month = 7
start_date, end_date = get_first_last_day(year, month)
print(f"Primer día: {start_date}")
print(f"Último día: {end_date}")

def get_series_times(row):
    try:
        base_code = row['code']
        query = {
            'base': base_code,
            'start_date': start_date,
            'end_date': end_date,
        }
        r = requests.get(base_url+'/timeseries', params=query)
        time_series = r.json()
        # print(time_series)
        return (
            time_series['start_date'] if 'start_date' in time_series else "N/A",
            time_series['end_date'] if 'end_date' in time_series else "N/A",
            json.dumps(time_series['rates'] if 'rates' in time_series else "N/A", ensure_ascii=False)
        )
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None, None, None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None, None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None, None
    
df_currencies['start_date'], df_currencies['end_date'], df_currencies['rates'] = zip(*df_currencies.apply(get_series_times, axis=1))

df_currencies['period'] = df_currencies['start_date'].str[:7]

known_currencies = [
    'USD', 'EUR', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'NZD',
    'BTC', 'ETH', 'BNB', 'XRP', 'SOL', 'DOT', 'ADA', 'USDT', 'USDC', 'ARS'
]
df_transform_data = df_currencies[df_currencies['code'].isin(known_currencies)]
df_time_series_values = pd.DataFrame()

for index, row in df_transform_data.iterrows():
    base_code = row['code']
    start_date = row['start_date']
    rates = row['rates']
    if rates and isinstance(rates, str):
        try:
            rates_dict = json.loads(rates)
            if isinstance(rates_dict, dict):
                for key, value in rates_dict.items():
                    # print(key)
                    # print(value)
                    df = pd.json_normalize(value)
                    df['code'] = base_code
                    df['date'] = key
                    df['period'] = key[:7]
                    df_time_series_values = pd.concat([df_time_series_values, df], ignore_index=True)
            else:
                print(f"Expected a dictionary but got {type(rates_dict)} for row {index}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON for row {index}")
        except TypeError:
            print(f"Type error for row {index}")

print(df_time_series_values)