import pynmea2, sqlite3, re
from datetime import datetime

DB = "/home/pi/gps_anomaly/data/gps_data.db"
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS gps_features (
    timestamp TEXT, lat REAL, lon REAL, fix_quality INTEGER,
    num_sats INTEGER, hdop REAL, prns TEXT, snr REAL
)''')
conn.commit()

def parse_gga(line):
    msg = pynmea2.parse(line)
    timestamp = datetime.utcnow().isoformat()
    return (
        timestamp,
        msg.latitude,
        msg.longitude,
        int(msg.gps_qual),
        int(msg.num_sats),
        float(msg.horizontal_dil),
        "",  # PRNs placeholder
        0.0  # SNR placeholder
    )

with open("/home/pi/gps_anomaly/logs/gps_log.nmea") as f:
    for line in f:
        try:
            if line.startswith('$GPGGA'):
                values = parse_gga(line)
                c.execute("INSERT INTO gps_features VALUES (?, ?, ?, ?, ?, ?, ?, ?)", values)
        except Exception:
            continue

conn.commit()
conn.close()
