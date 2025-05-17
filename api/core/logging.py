"""
Logging configuration for the API.
"""

import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

def setup_logging(log_dir=None, log_level=logging.INFO):
    """
    Set up logging for the API.
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level
    """
    # Create logger
    logger = logging.getLogger("compliance-advisor-api")
    logger.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log directory is provided
    if log_dir:
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_path / "api.log",
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Create default logger
logger = setup_logging()
