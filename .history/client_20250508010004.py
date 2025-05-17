import tkinter as tk
from tkinter import ttk
import requests

flask_url = "http://192.168.86.27:8080"

root = tk.Tk()
root.title("GPS Anomaly Detection Dashboard")
root.geometry("900x600")
root.configure(bg="#f8f8f8")

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook.Tab", font=("Helvetica", 11), padding=4)
style.configure("Compact.TLabel", font=("Helvetica", 9), background="#ffffff", anchor="w", relief="ridge")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=5, pady=5)

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
        ttk.Label(container, text="No data", style="Compact.TLabel").grid(row=0, column=0)
        return

    for row_idx, item in enumerate(data):
        for col_idx, (key, value) in enumerate(item.items()):
            ttk.Label(container, text=str(key), style="Compact.TLabel", width=12).grid(row=row_idx, column=2 * col_idx, sticky="nsew", padx=1, pady=1)
            ttk.Label(container, text=str(value), style="Compact.TLabel", width=16).grid(row=row_idx, column=2 * col_idx + 1, sticky="nsew", padx=1, pady=1)

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

    canvas = tk.Canvas(tab_frame, bg="#f8f8f8", highlightthickness=0)
    v_scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
    h_scrollbar = ttk.Scrollbar(tab_frame, orient="horizontal", command=canvas.xview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    canvas.pack(side="top", fill="both", expand=True)
    v_scrollbar.pack(side="right", fill="y")
    h_scrollbar.pack(side="bottom", fill="x")

    frames[endpoint] = {"scrollable_frame": scrollable_frame}

update_all()
root.mainloop()
