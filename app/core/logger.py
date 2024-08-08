import logging
from pathlib import Path


LOG_DIRECTORY = Path("logs")
Path.mkdir(LOG_DIRECTORY, exist_ok=True)
LOG_FILE = LOG_DIRECTORY / "server.log"


def set_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="[%(asctime)s]-[%(levelname)s|%(filename)s:%(lineno)s]-[%(message)s]",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=1024 * 1024 * 100, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = set_logger("nerdqa")
