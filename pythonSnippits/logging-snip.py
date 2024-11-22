import logging

# Setup Logging
logger = logging.getLogger()
logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG,
)

# Write to log
logger.debug(f"This is a debug message.")
logger.info(f"This is an informational message.")
logger.warning(f"This is a warning message!")
logger.error(f"This is an error message!")
logger.critical(f"This is a critical message!!!")
