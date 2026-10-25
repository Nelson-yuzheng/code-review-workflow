import os
from datetime import datetime

LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs"
)
os.makedirs(LOG_DIR, exist_ok=True)
_LOG_FILE = os.path.join(LOG_DIR, "workflow.log")


def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] [{level}] {message}"
    print(line)
    with open(_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    return line
