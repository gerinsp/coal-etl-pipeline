import pandas as pd

def validate_metrics(df):
    errors = []
    for i, row in df.iterrows():
        if row['total_production_daily'] < 0:
            errors.append((row['date'], 'Negative production'))
        if not (0 <= row['equipment_utilization'] <= 100):
            errors.append((row['date'], 'Equipment utilization out of range'))
        if pd.isnull(row['precipitation_sum']):
            errors.append((row['date'], 'Missing weather data'))

    with open('logs/etl_errors.log', 'w') as f:
        for error in errors:
            f.write(f"{error[0]} - {error[1]}\n")
