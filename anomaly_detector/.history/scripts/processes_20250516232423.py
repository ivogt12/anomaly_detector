import subprocess
import threading
import time
import sys

python_exec = sys.executable

def start_logging():
    subprocess.Popen(['/home/isarasb/gps_anomaly/scripts/start_logging.sh'])

def 