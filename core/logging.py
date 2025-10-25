"""
Logging configuration
"""
import logging
import sys
from core.config import settings


def setup_logging():
    """Setup application logging"""
    
    # Create logger
    logger = logging.getLogger("compagent")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


# Create default logger instance
logger = setup_logging()
