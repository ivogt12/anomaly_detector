import pynmea2

with open("gps_log.nmea") as file:
    for line in file:
        if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
            try:
                msg = pynmea2.parse(line)
                print(msg.latitude, msg.longitude, msg.timestamp)
            except pynmea2.nmea.ParseError:
                continue
