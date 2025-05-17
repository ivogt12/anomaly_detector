import tkinter as tk
from tkinter import ttk
import requests

flask_url = "http://192.168.86.27:8080"

root = tk.Tk()
root.title("GPS Anomaly Detection Dashboard")
root.geometry("1000x700")
root.configure(bg="#eaeaea")

# Style configuration
style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook.Tab", font=("Segoe UI", 11), padding=6)
style.configure("Data.TLabel", font=("Segoe UI", 9), background="#ffffff", anchor="w", relief="groove")
style.configure("Header.TLabel", font=("Segoe UI", 10, "bold"), background="#f0f0f0", anchor="center", relief="flat")
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

def display_data(data, container):
    clear_frame(container)

    # Object count
    count_label = ttk.Label(container, text=f"Items: {len(data)}", style="Count.TLabel", anchor="w")
    count_label.grid(row=0, column=0, columnspan=10, sticky="w", padx=5, pady=(5, 10))

    if not data:
        ttk.Label(container, text="No data available.", style="Data.TLabel").grid(row=1, column=0)
        return

    keys = list(data[0].keys())
    for col_idx, key in enumerate(keys):
        ttk.Label(container, text=key, style="Header.TLabel", width=15).grid(row=1, column=col_idx, sticky="nsew", padx=1, pady=2)

    for row_idx, item in enumerate(data, start=2):
        bg = "#ffffff" if row_idx % 2 == 0 else "#f9f9f9"
        for col_idx, key in enumerate(keys):
            cell = ttk.Label(container, text=str(item.get(key, "")), style="Data.TLabel", width=15)
            cell.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
            cell.configure(background=bg)

def update_all():
    for endpoint, frame_info in frames.items():
        scrollable_frame = frame_info["scrollable_frame"]
        data = fetch_data(endpoint)
        display_data(data, scrollable_frame)
    root.after(5000, update_all)

# Create tabs with scrollable frames
for endpoint, title in data_endpoints.items():
    tab_frame = ttk.Frame(notebook)
    notebook.add(tab_frame, text=title)

    # Canvas with scrollbar
    canvas = tk.Canvas(tab_frame, borderwidth=0, background="#eaeaea")
    v_scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=v_scrollbar.set)

    v_scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def _on_mousewheel(event, canvas=canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)

    frames[endpoint] = {"scrollable_frame": scrollable_frame}

update_all()
root.mainloop()
import tkinter as tk
from tkinter import ttk
import requests

flask_url = "http://192.168.86.27:8080"

root = tk.Tk()
root.title("GPS Anomaly Detection Dashboard")
root.geometry("1000x700")
root.configure(bg="#eaeaea")

# Style configuration
style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook.Tab", font=("Segoe UI", 11), padding=6)
style.configure("Data.TLabel", font=("Segoe UI", 9), background="#ffffff", anchor="w", relief="groove")
style.configure("Header.TLabel", font=("Segoe UI", 10, "bold"), background="#f0f0f0", anchor="center", relief="flat")
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

def display_data(data, container):
    clear_frame(container)

    # Object count
    count_label = ttk.Label(container, text=f"Items: {len(data)}", style="Count.TLabel", anchor="w")
    count_label.grid(row=0, column=0, columnspan=10, sticky="w", padx=5, pady=(5, 10))

    if not data:
        ttk.Label(container, text="No data available.", style="Data.TLabel").grid(row=1, column=0)
        return

    keys = list(data[0].keys())
    for col_idx, key in enumerate(keys):
        ttk.Label(container, text=key, style="Header.TLabel", width=15).grid(row=1, column=col_idx, sticky="nsew", padx=1, pady=2)

    for row_idx, item in enumerate(data, start=2):
        bg = "#ffffff" if row_idx % 2 == 0 else "#f9f9f9"
        for col_idx, key in enumerate(keys):
            cell = ttk.Label(container, text=str(item.get(key, "")), style="Data.TLabel", width=15)
            cell.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
            cell.configure(background=bg)

def update_all():
    for endpoint, frame_info in frames.items():
        scrollable_frame = frame_info["scrollable_frame"]
        data = fetch_data(endpoint)
        display_data(data, scrollable_frame)
    root.after(5000, update_all)

# Create tabs with scrollable frames
for endpoint, title in data_endpoints.items():
    tab_frame = ttk.Frame(notebook)
    notebook.add(tab_frame, text=title)

    # Canvas with scrollbar
    canvas = tk.Canvas(tab_frame, borderwidth=0, background="#eaeaea")
    v_scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=v_scrollbar.set)

    v_scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def _on_mousewheel(event, canvas=canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)

    frames[endpoint] = {"scrollable_frame": scrollable_frame}

update_all()
root.mainloop()

