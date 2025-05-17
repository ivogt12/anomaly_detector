from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/gps-log')
def gps_log():
    conn = sqlite3.connect('/home/isarasb/gps_anomaly/data/gps_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gps_log ORDER BY timestamp DESC LIMIT 5")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/snr-anomalies')
def snr_anomalies():
    conn = sqlite3.connect('/home/isarasb/gps_anomaly/data/gps_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM snr_anomalies ORDER BY timestamp DESC LIMIT 5")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/rare-prns')
def rare_prns():
    conn = sqlite3.connect('/home/isarasb/gps_anomaly/data/gps_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rare_prns ORDER BY count DESC LIMIT 5")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/iso-anomalies')
def iso_anomalies():
    conn = sqlite3.connect('/home/isarasb/gps_anomaly/data/gps_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM iso_anomalies ORDER BY timestamp DESC LIMIT 5")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/satellite-readings')
def satellite_readings():
    conn = sqlite3.connect('/home/isarasb/gps_anomaly/data/gps_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM satellite_readings ORDER BY timestamp DESC LIMIT 5")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
