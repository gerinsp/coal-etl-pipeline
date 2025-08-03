# Coal Mining Production Data Pipeline

A data pipeline to collect, transform, and load coal production metrics, integrated with Apache Doris and Metabase dashboard.

## 📦 Tech Stack

- Python (ETL)
- Apache Doris (Data Warehouse)
- Metabase (Dashboard)
- Docker & Docker Compose

## 🛠️ Pipeline Overview

1. **Extract**
   - SQL data (`production_logs` table)
   - Equipment sensor data (`equipment_sensors.csv`)
   - Weather data (Open-Meteo API)

2. **Transform**
   - Daily metrics: `total_production`, `avg_quality`, `utilization`, `fuel_efficiency`, `weather_impact`

3. **Load**
   - Store into `daily_production_metrics` table in ClickHouse

4. **Validate**
   - Anomaly & completeness checks, logged in `logs/etl_errors.log`

## 📊 Dashboard

Visualized using Metabase (see `dashboard/` folder for screenshots).

## 🚀 Setup (with Docker)

```bash
cd docker/
docker-compose up -d
