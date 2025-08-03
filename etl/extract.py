import pandas as pd
import requests
from datetime import datetime
from sqlalchemy import create_engine
from config.db_config import SQL_DB_URI

def extract_sql_data():
    engine = create_engine(SQL_DB_URI)
    query = "SELECT * FROM production_logs;"
    df = pd.read_sql(query, engine)
    return df

def extract_csv_data(filepath='data/equipment_sensors.csv'):
    return pd.read_csv(filepath)

def extract_weather_data(start_date, end_date):
    ALLOWED_START = datetime.strptime("2025-05-02", "%Y-%m-%d")
    ALLOWED_END = datetime.strptime("2025-08-18", "%Y-%m-%d")

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    if start_dt < ALLOWED_START:
        start_dt = ALLOWED_START
    if end_dt > ALLOWED_END:
        end_dt = ALLOWED_END

    start_date = start_dt.strftime("%Y-%m-%d")
    end_date = end_dt.strftime("%Y-%m-%d")

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude=2.0167&longitude=117.3000&daily=temperature_2m_mean,precipitation_sum"
        f"&timezone=Asia%2FJakarta&start_date={start_date}&end_date={end_date}"
    )

    print(f"[extract_weather_data] URL: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        print(response.text)
        raise Exception(f"API Error: {response.status_code}")

    data = response.json()["daily"]
    df = pd.DataFrame({
        "date": data["time"],
        "temperature_2m_mean": data["temperature_2m_mean"],
        "precipitation_sum": data["precipitation_sum"]
    })

    df["weather_impact"] = df["precipitation_sum"].apply(lambda x: 1 if x > 5 else 0)

    return df