import subprocess
import threading
import time
import sys

python_exec = sys.executable

def start_logging():
    subprocess.Popen(['/home/isarasb/gps_anomaly/scripts/start_logging.sh'])

def run_parser():
    subprocess.Popen([python_exec, '/home/isarasb/gps_anomaly/scripts/parser.py'])

def train_model_periodically():
    while True:
        subprocess.run([python_exec, ''])
        time.sleep(3600)

def cleanup_db_periodically():
    while True:
        subprocess.run([python_exec, ''])
        time.sleep(300)

if __name__ == "__main__":
    start_logging()
    run_parser()

    threading.Thread(target=train_model_periodically).start()
    threading.Thread(target=cleanup_db_periodically).start()

    while True:
        time.sleep(60)