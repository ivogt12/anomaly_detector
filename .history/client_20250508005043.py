import tkinter as tk
import requests
import json

# Your Flask server URL
flask_url = "http://192.168.86.27:5000"

# Create the Tkinter root window
root = tk.Tk()
root.title("GPS Anomaly Detection")

label = tk.Label(root, text="Loading...", font=("Courier", 14))
label.pack(padx=10, pady=20)

# Function to fetch data from the Flask API
def fetch_data(endpoint):
    try:
        response = requests.get(f"{flask_url}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch data"}
    except Exception as e:
        return {"error": str(e)}

# Function to update the display with fetched data
def update_display():
    # Get data from Flask API
    gps_log_data = fetch_data("gps-log")
    snr_anomalies = fetch_data("snr-anomalies")
    rare_prns = fetch_data("rare-prns")
    iso_anomalies = fetch_data("iso-anomalies")
    satellite_readings = fetch_data("satellite-readings")

    # Display data as a string
    display_text = f"""
GPS Log:
{json.dumps(gps_log_data, indent=2)}

SNR Anomalies:
{json.dumps(snr_anomalies, indent=2)}

Rare PRNs:
{json.dumps(rare_prns, indent=2)}

ISO Anomalies:
{json.dumps(iso_anomalies, indent=2)}

Satellite Readings:
{json.dumps(satellite_readings, indent=2)}
"""
    label.config(text=display_text)

    # Refresh every 5 seconds
    root.after(5000, update_display)

# Start the update loop
update_display()

# Run the Tkinter event loop
root.mainloop()
