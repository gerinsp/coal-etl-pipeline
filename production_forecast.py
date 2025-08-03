import pandas as pd
import pymysql
from prophet import Prophet
import matplotlib.pyplot as plt
import os
from config.db_config import DORIS_DB

# Koneksi ke Doris
conn = pymysql.connect(
    host=DORIS_DB['host'],
    port=9030,
    user=DORIS_DB['user'],
    password=DORIS_DB['password'],
    database=DORIS_DB['database']
)

# Query data historis produksi
query = """
SELECT date, total_production_daily
FROM daily_production_metrics
ORDER BY date
"""
df = pd.read_sql(query, conn)
conn.close()

# Buat folder output jika belum ada
os.makedirs("forecast", exist_ok=True)

# Format kolom agar sesuai Prophet
df.rename(columns={'date': 'ds', 'total_production_daily': 'y'}, inplace=True)
df['ds'] = pd.to_datetime(df['ds'])

# Inisialisasi dan latih model Prophet
model = Prophet()
model.fit(df)

# Prediksi 1 hari ke depan
future = model.make_future_dataframe(periods=1)
forecast = model.predict(future)

# Simpan hasil forecast ke CSV
forecast[['ds', 'yhat']].tail(1).to_csv("forecast/forecast_tomorrow.csv", index=False)

# Tampilkan hasil prediksi terakhir
print("📈 Prediksi Produksi Besok:")
print(forecast[['ds', 'yhat']].tail(1))

# Plot hasil prediksi
model.plot(forecast)
plt.title("Forecast Total Production")
plt.xlabel("Date")
plt.ylabel("Tons Extracted")
plt.tight_layout()

plt.savefig("forecast/forecast_plot.png")

plt.show()