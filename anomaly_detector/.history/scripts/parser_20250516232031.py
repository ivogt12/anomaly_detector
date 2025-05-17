import pynmea2
import sqlite3
import re
import time
from datetime import datetime

DB = "/home/isarasb/gps_anomaly/data/gps_data.db"
conn = sqlite3.connect(DB)
cursor = conn.cursor()

# Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS gps_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        latitude REAL,
        longitude REAL,
        num_sats INTEGER,
        fix_quality INTEGER,
        hdop REAL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS satellite_readings (
        timestamp TEXT,
        prn INTEGER,
        elevation INTEGER,
        azimuth INTEGER,
        snr REAL
    )
""")

conn.commit()

def parse_nmea():
    timestamp = None
    with open("/home/isarasb/gps_anomaly/logs/gps_log.nmea") as f:
        for _ in range(3):
            next(f)
        for line in f:
            try:
                if line.startswith("{P}")
                msg = pynmea2.parse(line)

                if isinstance(msg, pynmea2.types.talker.GGA):
                    timestamp = msg.timestamp.strftime("%H:%M:%S")
                    lat = msg.latitude
                    lon = msg.longitude
                    num_sats = msg.num_sats
                    fix_quality = msg.gps_qual
                    hdop = msg.horizontal_dil

                    cursor.execute("""
                        INSERT INTO gps_log (timestamp, latitude, longitude, num_sats, fix_quality, hdop)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (timestamp, lat, lon, num_sats, fix_quality, hdop))

                elif isinstance(msg, pynmea2.types.talker.GSV):
                    sat_data = msg.data[4:]
                    last_timestamp = timestamp or datetime.now().strftime("%H:%M:%S")
                    for i in range(0, len(sat_data), 4):
                        if i + 3 >= len(sat_data):
                            continue
                        try:
                            prn = int(sat_data[i])
                            elevation = int(sat_data[i + 1])
                            azimuth = int(sat_data[i + 2])
                            snr = float(sat_data[i + 3]) if sat_data[i + 3] != '' else None
                            if prn and snr is not None:
                                cursor.execute("""
                                    INSERT INTO satellite_readings (timestamp, prn, elevation, azimuth, snr)
                                    VALUES (?, ?, ?, ?, ?)
                                """, (last_timestamp, prn, elevation, azimuth, snr))
                        except (ValueError, pynmea2.ParseError) as e:
                            print(f"Satellite data parsing error: {e}")
                            continue
            except pynmea2.ParseError as e:
                print(f"Parsing error occurred: {e}")
                continue
    conn.commit()

while True:
    parse_nmea()
    time.sleep(1)
