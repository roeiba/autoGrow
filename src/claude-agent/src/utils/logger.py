"""Logging configuration for Claude Agent"""

import logging
import sys
from datetime import datetime


def setup_logger(name: str = "claude-agent", level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a logger instance
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Format: [2024-11-13 10:30:45] INFO: Message
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = "claude-agent") -> logging.Logger:
    """Get or create a logger instance"""
    return logging.getLogger(name)
