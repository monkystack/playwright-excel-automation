import logging
from logging.handlers import RotatingFileHandler
import functools
import time
import os

# ----------------------------
# Ensure log directory exists
# ----------------------------
LOG_DIR = "logs/python"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, "py.log")

# ----------------------------
# Rolling File Handler
# - max size: 2MB
# - max backups: 5
# ----------------------------
file_handler = RotatingFileHandler(
    LOG_PATH,
    maxBytes=2 * 1024 * 1024,   # 2 MB
    backupCount=5,              # py.log.1 ~ py.log.5
    encoding="utf-8"
)

# Console output handler
console_handler = logging.StreamHandler()

# Log format
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# ----------------------------
# root logger config
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)

# ----------------------------
# global logger (main.py uses this)
# ----------------------------
logger = logging.getLogger("automation")


# ===========================================================
# Decorator: auto log entry, exit, time, exception
# ===========================================================
def auto_log(func):
    """
    Decorator that automatically logs:
    - function entry
    - function exit
    - execution time
    - any exception
    """
    func_logger = logging.getLogger(func.__module__)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_logger.info(f"➡️ Enter: {func.__name__}")
        start = time.time()

        try:
            result = func(*args, **kwargs)
            duration = (time.time() - start) * 1000
            func_logger.info(f"⬅️ Exit: {func.__name__} ({duration:.1f} ms)")
            return result

        except Exception as e:
            func_logger.exception(f"💥 Exception in {func.__name__}: {e}")
            raise

    return wrapper