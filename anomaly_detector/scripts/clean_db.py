import sqlite3
import time  # <- you forgot to import this

def cleanup_db():
    conn = sqlite3.connect('/home/isarasb/gps_anomaly/data/gps_data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gps_log WHERE timestamp < datetime('now', '-1 day')")
    conn.commit()
    conn.close()

# Run cleanup periodically (e.g., every 5 minutes)
while True:
    cleanup_db()
    time.sleep(300)  # 5 minutes
