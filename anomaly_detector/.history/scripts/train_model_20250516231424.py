from sklearn.ensemble import IsolationForest
import pandas as pd
import sqlite3

conn = sqlite3.connect("/home/pi/gps_anomaly/data/gps_data.db")
df = pd.read_sql_query("SELECT * FROM gps_features ORDER BY timestamp DESC LIMIT 100", conn)

X = df[['lat', 'lon', 'hdop', 'num_sats']].dropna()
model = IsolationForest()
model.fit(X)
df['anomaly'] = model.predict(X)

df.to_csv("/home/pi/gps_anomaly/data/latest_results.csv", index=False)
conn.close()
