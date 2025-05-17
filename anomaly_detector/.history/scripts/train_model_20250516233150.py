import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Load satellite data
conn = sqlite3.connect('/home/isarasb/gps_anomaly/gps_data.db')
cursor
# Ensure required tables exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS gps_log (
    timestamp TEXT,
    latitude REAL,
    longitude REAL,
    num_sats INTEGER,
    fix_quality INTEGER,
    hdop REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS satellite_readings (
    timestamp TEXT,
    prn INTEGER,
    elevation INTEGER,
    azimuth INTEGER,
    snr REAL
)
""")

df = pd.read_sql_query("SELECT * FROM satellite_readings", conn)
conn.close()

print("Total satellite records loaded:", len(df))

# ------------------ SNR DROP DETECTION ------------------
print("\n🔍 SNR Drop Anomalies:")
for prn in df['prn'].unique():
    prn_df = df[df['prn'] == prn].sort_values(by='timestamp')
    prn_df['snr_diff'] = prn_df['snr'].diff()
    drops = prn_df[prn_df['snr_diff'] < -5]
    if not drops.empty:
        print(f"\nPRN {prn} had significant SNR drops:")
        print(drops[['timestamp', 'snr', 'snr_diff']])

# ------------------ RARE PRN DETECTION ------------------
print("\n🔍 Rarely Seen PRNs:")
prn_counts = df['prn'].value_counts()
rare_prns = prn_counts[prn_counts < prn_counts.mean() - prn_counts.std()]
print(rare_prns)

# ------------------ ISOLATION FOREST ------------------
print("\n🔍 Statistical Outliers (Isolation Forest):")
features = df[['snr', 'elevation', 'azimuth']].dropna()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

iso = IsolationForest(contamination=0.05, random_state=42)
df = df.iloc[features.index]  # match index after dropna
df['anomaly'] = iso.fit_predict(X_scaled)

anomalies = df[df['anomaly'] == -1]
print(f"\nTotal anomalies detected: {len(anomalies)}")
print(anomalies[['timestamp', 'prn', 'snr', 'elevation', 'azimuth']])
