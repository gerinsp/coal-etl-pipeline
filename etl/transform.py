import pandas as pd

def transform_metrics(production_df, sensor_df, weather_dict):
    production_df['date'] = pd.to_datetime(production_df['date'])
    sensor_df['timestamp'] = pd.to_datetime(sensor_df['timestamp'])
    sensor_df['date'] = sensor_df['timestamp'].dt.normalize()

    production_df.loc[production_df['tons_extracted'] < 0, 'tons_extracted'] = 0

    daily_total = production_df.groupby(['date', 'mine_id'])['tons_extracted'].sum().reset_index(name='total_production_daily')
    daily_quality = production_df.groupby(['date', 'mine_id'])['quality_grade'].mean().reset_index(name='average_quality_grade')

    sensor_df = sensor_df.merge(
        production_df[['date', 'mine_id']].drop_duplicates(),
        on=['date'], how='left'
    )

    equipment_utilization = sensor_df.groupby(['date', 'mine_id'])['status'].apply(
        lambda x: (x == 'active').sum() / len(x) * 100
    ).reset_index(name='equipment_utilization')

    total_fuel = sensor_df.groupby(['date', 'mine_id'])['fuel_consumption'].sum().reset_index(name='total_fuel')
    fuel_eff = pd.merge(daily_total, total_fuel, on=['date', 'mine_id'], how='left')
    fuel_eff['fuel_efficiency'] = fuel_eff['total_fuel'] / fuel_eff['total_production_daily']
    fuel_eff = fuel_eff[['date', 'mine_id', 'fuel_efficiency']]

    per_mine_df = daily_total \
        .merge(daily_quality, on=['date', 'mine_id']) \
        .merge(equipment_utilization, on=['date', 'mine_id']) \
        .merge(fuel_eff, on=['date', 'mine_id'])

    per_mine_df['equipment_utilization'] = per_mine_df['equipment_utilization'].clip(0, 100)
    per_mine_df['fuel_efficiency'] = per_mine_df['fuel_efficiency'].fillna(0)

    weather_df = pd.DataFrame(weather_dict)
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    per_mine_df = per_mine_df.merge(weather_df, on='date', how='left')

    main_df = per_mine_df.groupby('date').agg({
        'total_production_daily': 'sum',
        'average_quality_grade': 'mean',
        'equipment_utilization': 'mean',
        'fuel_efficiency': 'mean',
        'temperature_2m_mean': 'mean',
        'precipitation_sum': 'mean'
    }).reset_index()

    weather_impact = main_df['precipitation_sum'].corr(main_df['total_production_daily'])
    main_df['weather_impact'] = weather_impact

    return main_df, per_mine_df