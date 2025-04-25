"""
Logging configuration for the application.
"""

import logging
import sys
from typing import Optional


def setup_logger(name: str, log_level: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with the specified name and level.
    
    Args:
        name (str): Name of the logger.
        log_level (Optional[str]): Log level as a string. Defaults to INFO if not specified.
        
    Returns:
        logging.Logger: Configured logger.
    """
    # Determine log level
    if log_level is None:
        level = logging.INFO
    else:
        level = getattr(logging, log_level.upper())
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create console handler if no handlers exist
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
    
    return logger


# Create a default application logger
logger = setup_logger("julep_research_assistant")