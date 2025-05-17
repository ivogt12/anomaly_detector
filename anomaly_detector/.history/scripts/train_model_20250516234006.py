import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Load satellite data
conn = sqlite3.connect("/home/isarasb/gps_anomaly/data/gps_data.db")

df = pd.read_sql_query("SELECT * FROM satellite_readings", conn)
conn.close()

print("Total satellite records loaded:", len(df))

# ------------------ Check Missing Values After Conversion ------------------
print("\nMissing Values After Type Conversion:")
print(df.isnull().sum())  # Check again after conversion

# ------------------ SNR DROP DETECTION ------------------
print("\n🔍 SNR Drop Anomalies:")

# Drop rows where 'snr' is NaN after conversion
df = df.dropna(subset=['snr'])

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

# Check if there are valid rows for scaling
if features.empty:
    print("No valid data for SNR, elevation, or azimuth after dropping NaNs.")
else:
    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # Run Isolation Forest for anomaly detection
    iso = IsolationForest(contamination=0.05, random_state=42)
    df = df.iloc[features.index]  # Match the index after dropna
    df['anomaly'] = iso.fit_predict(X_scaled)

    # Print anomalies detected by Isolation Forest
    anomalies = df[df['anomaly'] == -1]
    print(f"\nTotal anomalies detected: {len(anomalies)}")
    print(anomalies[['timestamp', 'prn', 'snr', 'elevation', 'azimuth']])