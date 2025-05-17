from sklearn.ensemble import IsolationForest
import pandas as pd

# Example: Read last 100 data points
df = pd.read_sql_query("SELECT * FROM gps_features ORDER BY timestamp DESC LIMIT 100", conn)

# Preprocess for model
X = df[['lat', 'lon', 'hdop', 'num_sats']].dropna()
model = IsolationForest()
model.fit(X)

# Predict anomalies
df['anomaly'] = model.predict(X)
