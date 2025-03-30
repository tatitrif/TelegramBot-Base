import asyncio
import logging
import os
from logging.handlers import QueueHandler, QueueListener, TimedRotatingFileHandler
from queue import Queue

log_folder = "logs"
info_log_file = os.path.join(log_folder, "info.log")
warning_log_file = os.path.join(log_folder, "warning.log")
error_log_file = os.path.join(log_folder, "error.log")

logs_files = [info_log_file, warning_log_file, error_log_file]

# Check if the log files exist and create them if they don't exist
for log_file in logs_files:
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            pass


# Custom filter to filter log records based on severity level
class SeverityFilter(logging.Filter):
    def __init__(self, severity):
        super().__init__()
        self.severity = severity

    def filter(self, record):
        return record.levelno == self.severity


# Set up logging
logging.basicConfig(level=logging.NOTSET)

# Create a formatter
formatter = logging.Formatter(
    "[%(asctime)s] - %(levelname)s - %(filename)s:%(lineno)d - %(name)s - %(message)s"
)


# Define a function to set up a TimedRotatingFileHandler
def create_timed_rotating_handler(
    log_filename, level, fmt, when="midnight", backup_count=7
):
    handler = TimedRotatingFileHandler(
        filename=log_filename, when=when, backupCount=backup_count
    )
    handler.setLevel(level)
    handler.setFormatter(fmt)
    handler.addFilter(SeverityFilter(level))
    return handler


# helper coroutine to set_up and manage the logger
async def init_logger():
    # Create handlers for each level using the reusable function
    info_handler = create_timed_rotating_handler(info_log_file, logging.INFO, formatter)
    warning_handler = create_timed_rotating_handler(
        warning_log_file, logging.WARNING, formatter
    )
    error_handler = create_timed_rotating_handler(
        error_log_file, logging.ERROR, formatter
    )

    # Create a Queue for log records
    log_queue = Queue()

    # Set up QueueHandler
    queue_handler = QueueHandler(log_queue)

    # Add the QueueHandler to the logger
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)  # Ensure logger captures all levels
    logger.handlers = []  # Clear any existing handlers to avoid duplicates
    logger.addHandler(queue_handler)

    # Set up QueueListener with the actual handlers
    listener = QueueListener(log_queue, info_handler, warning_handler, error_handler)

    # Add StreamHandler for console logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Set to DEBUG for console
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    try:
        # start the listener
        listener.start()
        # report the logger is ready
        logging.debug("Logger has started")
        # wait forever
        while True:
            await asyncio.sleep(60)
    except Exception as err:
        logging.error(f"{err}")

    finally:
        # report the logger is done
        logging.debug("Logger is shutting down")
        # ensure the listener is closed
        listener.stop()


# coroutine to safely start the logger
async def safely_start_logger():
    # initialize the logger
    asyncio.create_task(init_logger())
    # allow the logger to start
    await asyncio.sleep(0)
