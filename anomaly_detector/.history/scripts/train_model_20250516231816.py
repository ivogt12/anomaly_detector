import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest

# Connect to the SQLite database
conn = sqlite3.connect("gps_data.db")

# Read all rows into a DataFrame
df = pd.read_sql_query("SELECT timestamp, latitude, longitude, num_sats, fix_quality, hdop FROM gps_log", conn)
conn.close()

# Drop any rows with missing values
df.dropna(inplace=True)

# Select numeric features only
features = df[['latitude', 'longitude', 'num_sats', 'fix_quality', 'hdop']]

# Train Isolation Forest
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
df['anomaly'] = model.fit_predict(features)

# Print anomalies
anomalies = df[df['anomaly'] == -1]
print("Anomalies detected:")
print(anomalies[['timestamp', 'latitude', 'longitude', 'num_sats', 'fix_quality', 'hdop']])
