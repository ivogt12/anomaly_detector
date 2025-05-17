import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import requests
import json

flask_url = "http://192.168.86.27:8080"

# Main Window
root = tk.Tk()
root.title("GPS Anomaly Detection Dashboard")
root.geometry("900x600")
root.configure(bg="#f5f5f5")

style = ttk.Style()
style.theme_use("clam")  # More modern themes: 'alt', 'clam', 'default', 'classic'
style.configure("TNotebook", background="#ffffff", borderwidth=0)
style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"), padding=[10, 5])
style.configure("TLabel", background="#f5f5f5", font=("Helvetica", 12))

# Tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# Create text widgets for each tab
tabs = {}
data_labels = {
    "gps-log": "GPS Log",
    "snr-anomalies": "SNR Anomalies",
    "rare-prns": "Rare PRNs",
    "iso-anomalies": "ISO Anomalies",
    "satellite-readings": "Satellite Readings"
}

for endpoint, label in data_labels.items():
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=label)
    scrolled_text = ScrolledText(frame, wrap=tk.WORD, font=("Courier", 10), state="disabled", bg="#f0f0f0")
    scrolled_text.pack(fill='both', expand=True, padx=10, pady=10)
    tabs[endpoint] = scrolled_text

# Status label
status = ttk.Label(root, text="Fetching data...", anchor="center")
status.pack(pady=(0, 10))

# Data fetching function
def fetch_data(endpoint):
    try:
        response = requests.get(f"{flask_url}/{endpoint}", timeout=3)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error {response.status_code}: Failed to fetch {endpoint}"}
    except Exception as e:
        return {"error": str(e)}

# Update function
def update_display():
    status.config(text="Refreshing...")
    root.update_idletasks()

    for endpoint in tabs:
        data = fetch_data(endpoint)
        text_widget = tabs[endpoint]
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, json.dumps(data, indent=2))
        text_widget.config(state="disabled")

    status.config(text="Last updated.")
    root.after(5000, update_display)  # Auto-refresh every 5 seconds

# Start update loop
update_display()
root.mainloop()
