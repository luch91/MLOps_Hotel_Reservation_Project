import logging
import os
from datetime import datetime

# Create a logger
LOGS_DIR = 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, f"{datetime.now()}")