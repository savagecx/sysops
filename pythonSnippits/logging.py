import logging

# Setup Logging
logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)

# Write to log
logging.log(f"This message will be logged with the default level.")
logging.debug(f"This is a debug message.")
logging.info(f"This is an informational message.")
logging.warning(f"This is a warning message!")
logging.error(f"This is an error message!")
logging.critical(f"This is a critical message!!!")
