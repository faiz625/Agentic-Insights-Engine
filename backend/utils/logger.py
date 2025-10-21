from loguru import logger
import sys
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure loguru once
logger.remove()
logger.add(sys.stderr, level=LOG_LEVEL, backtrace=False, diagnose=False)
