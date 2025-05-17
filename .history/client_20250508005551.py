import tkinter as tk
from tkinter import ttk
import requests

flask_url = "http://192.168.86.27:8080"

root = tk.Tk()
root.title("GPS Anomaly Detection Dashboard")
root.geometry("1000x700")
root.configure(bg="#f5f5f5")

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"), padding=[10, 5])
style.configure("TLabel", background="#ffffff", font=("Helvetica", 10), relief="groove", padding=5)

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

data_endpoints = {
    "gps-log": "GPS Log",
    "snr-anomalies": "SNR Anomalies",
    "rare-prns": "Rare PRNs",
    "iso-anomalies": "ISO Anomalies",
    "satellite-readings": "Satellite Readings"
}

frames = {}

def fetch_data(endpoint):
    try:
        res = requests.get(f"{flask_url}/{endpoint}", timeout=3)
        if res.status_code == 200:
            return res.json()
        return [{"error": f"Failed to fetch: {res.status_code}"}]
    except Exception as e:
        return [{"error": str(e)}]

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def display_data(data, container):
    clear_frame(container)
    if not data:
        ttk.Label(container, text="No data").grid(row=0, column=0)
        return

    for row_idx, item in enumerate(data):
        for col_idx, (key, value) in enumerate(item.items()):
            key_label = ttk.Label(container, text=str(key), background="#e6e6e6", anchor="w", width=20)
            val_label = ttk.Label(container, text=str(value), background="#ffffff", anchor="w", width=40)
            key_label.grid(row=row_idx, column=2 * col_idx, sticky="nsew", padx=2, pady=2)
            val_label.grid(row=row_idx, column=2 * col_idx + 1, sticky="nsew", padx=2, pady=2)

def update_all():
    for endpoint, frame_info in frames.items():
        scrollable_frame = frame_info["scrollable_frame"]
        data = fetch_data(endpoint)
        display_data(data, scrollable_frame)
    root.after(5000, update_all)

# Create tabs
for endpoint, title in data_endpoints.items():
    tab_frame = ttk.Frame(notebook)
    notebook.add(tab_frame, text=title)

    canvas = tk.Canvas(tab_frame, bg="#ffffff")
    scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    frames[endpoint] = {"scrollable_frame": scrollable_frame}

update_all()
root.mainloop()
