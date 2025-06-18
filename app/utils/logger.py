import logging
from logging.handlers import TimedRotatingFileHandler
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)


# 設定 error logger
error_logger = logging.getLogger("task_api_error")
error_logger.setLevel(logging.ERROR)
error_handler = TimedRotatingFileHandler(
    filename=os.path.join(log_dir, "error.log"),
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8",
)
error_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s %(name)s %(filename)s %(lineno)d")
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)
error_logger.propagate = False

# 設定 access logger
access_logger = logging.getLogger("task_api_access")
access_logger.setLevel(logging.INFO)
access_handler = TimedRotatingFileHandler(
    filename=os.path.join(log_dir, "access.log"),
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8",
)
access_formatter = logging.Formatter("%(asctime)s - %(message)s")
access_handler.setFormatter(access_formatter)
access_logger.addHandler(access_handler)
access_logger.propagate = False
