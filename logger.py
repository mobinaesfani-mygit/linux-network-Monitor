"""
Logging configuration for the network monitor.

This module creates JSON log messages and writes them
to both a log file and the console.
"""

import json
import logging
import os
from datetime import datetime, timezone

from config import LOG_FILE, LOG_LEVEL


class JsonFormatter(logging.Formatter):
    """
    Format log records as JSON.

    Each log entry contains a timestamp, log level,
    message, host, port, status, response time, and error.
    """

    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "host": getattr(record, "host", None),
            "port": getattr(record, "port", None),
            "status": getattr(record, "status", None),
            "response_time_ms": getattr(
                record, "response_time_ms", None
            ),
            "error": getattr(record, "error", None),
        }

        return json.dumps(log_data)


def setup_logger():
    """
    Create and configure the project logger.

    The logger writes JSON messages to a file and
    to the console.

    Returns:
        logging.Logger: Configured logger instance.
    """

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    logger = logging.getLogger("network_monitor")
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = JsonFormatter()

    # Write logs to a file
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    # Display logs in the terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger