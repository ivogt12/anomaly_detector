import tkinter as tk
from tkinter import ttk
import requests

flask_url = "http://192.168.86.27:8080"

root = tk.Tk()
root.title("GPS Anomaly Detection Dashboard")
root.geometry("1100x700")
root.configure(bg="#eaeaea")

# Style configuration
style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook.Tab", font=("Segoe UI", 11), padding=6)
style.configure("Data.TLabel", font=("Segoe UI", 9), background="#ffffff", anchor="w", relief="groove")
style.configure("Header.TLabel", font=("Segoe UI", 10, "bold"), background="#dbe9ff", anchor="center", relief="flat")
style.configure("Count.TLabel", font=("Segoe UI", 10, "italic"), background="#e0f7fa")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=6, pady=6)

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

def display_data(data, header_frame, scrollable_frame):
    clear_frame(header_frame)
    clear_frame(scrollable_frame)

    ttk.Label(header_frame, text=f"Items: {len(data)}", style="Count.TLabel").pack(anchor="w", pady=(5, 2), padx=6)

    if not data:
        ttk.Label(scrollable_frame, text="No data available.", style="Data.TLabel").grid(row=0, column=0)
        return

    keys = list(data[0].keys())
    for col_idx, key in enumerate(keys):
        ttk.Label(header_frame, text=key, style="Header.TLabel", width=15).pack(side="left", padx=1)

    for row_idx, item in enumerate(data):
        bg = "#ffffff" if row_idx % 2 == 0 else "#f7faff"
        for col_idx, key in enumerate(keys):
            label = ttk.Label(scrollable_frame, text=str(item.get(key, "")), style="Data.TLabel", width=15)
            label.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
            label.configure(background=bg)

def update_all():
    for endpoint, frame_info in frames.items():
        header = frame_info["header"]
        scrollable = frame_info["scrollable"]
        data = fetch_data(endpoint)
        display_data(data, header, scrollable)
    root.after(5000, update_all)

# Create tabs
for endpoint, title in data_endpoints.items():
    tab_frame = ttk.Frame(notebook)
    notebook.add(tab_frame, text=title)

    # Header (fixed)
    header_frame = ttk.Frame(tab_frame)
    header_frame.pack(fill="x", padx=5, pady=(5, 0))

    # Scrollable body
    canvas = tk.Canvas(tab_frame, borderwidth=0, background="#eaeaea", height=600)
    v_scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=v_scrollbar.set)

    v_scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scrollable_frame = ttk.Frame(canvas)
    canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def _on_mousewheel(event, canvas=canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    scrollable_frame.bind("<Configure>", lambda e, c=canvas: canvas.configure(scrollregion=c.bbox("all")))
    scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)

    frames[endpoint] = {
        "header": header_frame,
        "scrollable": scrollable_frame
    }

update_all()
root.mainloop()
