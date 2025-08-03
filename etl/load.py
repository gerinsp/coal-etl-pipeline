import pandas as pd

def load_to_doris(df: pd.DataFrame, table_name: str):
    import pymysql
    from config.db_config import DORIS_DB

    conn = pymysql.connect(
        host=DORIS_DB['host'],
        user=DORIS_DB['user'],
        password=DORIS_DB['password'],
        port=DORIS_DB['port'],
        autocommit=True
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DORIS_DB['database']};")
    cursor.close()
    conn.close()

    conn = pymysql.connect(
        host=DORIS_DB['host'],
        user=DORIS_DB['user'],
        password=DORIS_DB['password'],
        port=DORIS_DB['port'],
        database=DORIS_DB['database'],
        autocommit=True
    )
    cursor = conn.cursor()

    if table_name == 'daily_production_metrics':
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            date DATE,
            total_production_daily FLOAT,
            average_quality_grade FLOAT,
            equipment_utilization FLOAT,
            fuel_efficiency FLOAT,
            temperature_2m_mean FLOAT,
            precipitation_sum FLOAT,
            weather_impact FLOAT
        )
        ENGINE=OLAP
        DUPLICATE KEY(date)
        DISTRIBUTED BY HASH(date) BUCKETS 1
        PROPERTIES ("replication_num" = "1");
        """
        insert_query = f"""
        INSERT INTO {table_name} (
            date, total_production_daily, average_quality_grade,
            equipment_utilization, fuel_efficiency,
            temperature_2m_mean, precipitation_sum, weather_impact
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        df = df[[
            'date',
            'total_production_daily',
            'average_quality_grade',
            'equipment_utilization',
            'fuel_efficiency',
            'temperature_2m_mean',
            'precipitation_sum',
            'weather_impact'
        ]]
    elif table_name == 'production_per_mine':
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            date DATE,
            mine_id INT,
            average_quality_grade FLOAT
        )
        ENGINE=OLAP
        DUPLICATE KEY(date, mine_id)
        DISTRIBUTED BY HASH(date, mine_id) BUCKETS 1
        PROPERTIES ("replication_num" = "1");
        """
        insert_query = f"""
        INSERT INTO {table_name} (
            date, mine_id, average_quality_grade
        ) VALUES (%s, %s, %s)
        """
        df = df[[
            'date',
            'mine_id',
            'average_quality_grade'
        ]]
    else:
        raise ValueError("Unknown table name")

    cursor.execute(create_query)

    df = df.astype(object).where(pd.notnull(df), None)

    df['date'] = pd.to_datetime(df['date']).dt.date.astype(str)

    data = [
        [None if isinstance(x, float) and pd.isna(x) else x for x in row]
        for row in df.values.tolist()
    ]

    cursor.executemany(insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()