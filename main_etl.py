from etl.extract import extract_sql_data, extract_csv_data, extract_weather_data
from etl.transform import transform_metrics
from etl.load import load_to_doris
from etl.validate import validate_metrics
import pandas as pd

def main():
    production_df = extract_sql_data()
    sensor_df = extract_csv_data()

    production_df['date'] = pd.to_datetime(production_df['date'])
    dates = production_df['date'].dt.strftime('%Y-%m-%d')
    start_date = dates.min()
    end_date = dates.max()

    weather = extract_weather_data(start_date, end_date)

    main_df, per_mine_df = transform_metrics(production_df, sensor_df, weather)

    validate_metrics(main_df)
    
    load_to_doris(main_df, table_name='daily_production_metrics')
    load_to_doris(per_mine_df, table_name='production_per_mine')

if __name__ == "__main__":
    main()
