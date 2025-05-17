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

✅ Solution: Use a Virtual Environment (Recommended & Safe)
Install the necessary tooling (only once):

bash
Copy
Edit
sudo apt update
sudo apt install python3-venv python3-pip python3-full
Create and activate a virtual environment:

bash
Copy
Edit
python3 -m venv ~/myenv
source ~/myenv/bin/activate
Install your packages safely inside the venv:

bash
Copy
Edit
pip install pynmea2 scikit-learn pandas numpy matplotlib