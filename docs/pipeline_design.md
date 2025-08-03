# 📊 Coal Production ETL Pipeline

**Author**: Gerin Sena Pratama  
**Challenge from**: PT Synapsis Sinergi Digital (AI Engineer Assessment)  
**Date**: August 2025

---

## 🧩 1. Overview

This ETL (Extract, Transform, Load) pipeline processes coal mining production data collected from multiple sources: MySQL database, CSV files containing equipment sensor data, and external weather API. The cleaned and transformed data is loaded into Apache Doris (data warehouse) for further analysis and visualization using Metabase. Additionally, a forecasting module predicts future production trends.

---

## 🗃️ 2. Data Sources

| Source Type | Source Name             | Description                                    |
|-------------|-------------------------|------------------------------------------------|
| SQL         | `production_logs`       | Coal production data per mine, shift, and date |
| CSV         | `equipment_sensors.csv` | Equipment sensor data: temperature, vibration, moisture, etc. |
| API         | Open-Meteo Weather API  | Daily weather data (temperature, precipitation) for Kalimantan region |

---

## ⚙️ 3. ETL Pipeline Stages

### Extract
- Retrieve production data from MySQL using SQLAlchemy (`production_logs` table)
- Load sensor data from `equipment_sensors.csv` via pandas
- Fetch daily weather data from Open-Meteo API

### Transform
- Clean and merge datasets, handling missing or invalid values
- Calculate metrics:
  - `total_production_daily` (tons/day)
  - `average_quality_grade` (quality per day/mine)
  - `equipment_utilization` (% of active equipment)
  - `fuel_efficiency` (fuel consumption per ton)
  - Weather impact variables (`precipitation_sum`, `temperature_2m_mean`)

### Validate
- Verify production values are non-negative
- Ensure equipment utilization is within 0–100%
- Log anomalies and errors to `logs/etl_errors.log`

### Load
- Insert processed data into Apache Doris tables:
  - `daily_production_metrics`
  - `production_per_mine`

---

## 🏗️ 4. Database Schema

### `daily_production_metrics`

| Column                 | Type    | Description                          |
|------------------------|---------|------------------------------------|
| date                   | DATE    | Production date                    |
| total_production_daily  | FLOAT   | Total coal production (tons)       |
| average_quality_grade   | FLOAT   | Average quality score per day      |
| equipment_utilization   | FLOAT   | Percentage of equipment active     |
| fuel_efficiency        | FLOAT   | Fuel consumption per ton produced  |
| temperature_2m_mean     | FLOAT   | Average daily temperature (°C)     |
| precipitation_sum      | FLOAT   | Daily total precipitation (mm)     |
| weather_impact         | FLOAT   | Derived metric showing weather effect on production |

### `production_per_mine`

| Column               | Type  | Description                        |
|----------------------|-------|----------------------------------|
| date                 | DATE  | Production date                  |
| mine_id              | INT   | Identifier for each mine          |
| average_quality_grade | FLOAT | Average quality grade per mine    |

---

## 🧰 5. Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python | Core ETL |
| SQLAlchemy | Koneksi ke MySQL |
| Pandas | Transformasi data |
| ClickHouse | Data warehouse |
| Metabase | Dashboard visualisasi |
| Docker Compose | Orkestrasi layanan lokal |
| Logging | Logging error & validasi |

---

## 📊 6. Visualization (Metabase)

Dashboards created using Metabase include:  
- Daily coal production trends (line chart)  
- Average quality by mine (bar chart)  
- Weather impact correlations (scatter plots)  

Accessible at: `http://localhost:3000`


---

## 🚀 7. How to Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker-compose up -d
python main_etl.py
```

---

## 📁 8. Project Structure

```bash
.
├── main_etl.py                      # Entrypoint ETL script
├── production_forecast.py           # Forecasting script using Prophet
├── config/
│   └── db_config.py                 # Database configuration
├── etl/
│   ├── extract.py                   # Extraction logic
│   ├── transform.py                 # Transformation logic
│   ├── load.py                      # Loading data to Doris
│   └── validate.py                  # Data validation and logging
├── mysql-init/
│   └── production_logs.sql          # Initial raw production data for MySQL
├── data/
│   └── equipment_sensors.csv        # Sensor data CSV
├── forecast/
│   ├── forecast_plot.png
│   └── forecast_tomorrow.csv        # Forecast outputs
├── logs/
│   └── etl_errors.log               # Validation and error logs
├── docker-compose.yml               # Docker Compose config for services
├── Dockerfile                      # Dockerfile for ETL process containerization
├── requirements.txt                # Python dependencies
├── docs/
│   ├── documentation_report.md     # Detailed project documentation
│   └── pipeline_design.md          # ETL pipeline design document
└── README.md                       # Project README

```

---

## 📌 9. Notes

- This project is part of an AI Engineer technical challenge by PT Synapsis Sinergi Digital.
- Forecasting and visualization modules are optional extensions.
- Docker setup requires manual import of initial data before running ETL.
- Validation and logging are implemented to ensure data quality.

---