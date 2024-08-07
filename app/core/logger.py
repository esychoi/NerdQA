import os
from pathlib import Path

import logging
from logging.config import dictConfig


LOG_DIRECTORY = "logs"
os.makedirs(LOG_DIRECTORY, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "encoding": "utf-8",
    "formatters": {
        "simple": {
            "format": "[%(asctime)s]-[%(levelname)s|%(filename)s:%(lineno)s]-[%(message)s]",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "maxBytes": 1024 * 1024 * 100,
            "filename": Path(LOG_DIRECTORY) / "server.log",
            "backupCount": 5,
        },
    },
    "loggers": {
        "intent_logger": {
            "handlers": ["console", "logfile"],
            "level": "INFO",
        }
    },
}


logger = logging.getLogger("nerd_qa")
dictConfig(LOGGING)
