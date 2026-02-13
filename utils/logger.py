"""
Custom Logger
Centralized logging utility using loguru
"""
import sys
from pathlib import Path
from loguru import logger
from config.config import Config


class CustomLogger:
    """Custom logger class with enhanced logging capabilities"""
    
    def __init__(self, name: str = "framework"):
        self.name = name
        self._configure_logger()
    
    def _configure_logger(self):
        """Configure logger with custom settings"""
        # Remove default logger
        logger.remove()
        
        # Console handler with color
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
            level=Config.LOG_LEVEL,
            colorize=True
        )
        
        # File handler for all logs
        logger.add(
            Config.LOG_DIR / "framework.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG",
            rotation="10 MB",
            retention="10 days",
            compression="zip"
        )
        
        # File handler for errors only
        logger.add(
            Config.LOG_DIR / "errors.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="ERROR",
            rotation="5 MB",
            retention="30 days",
            compression="zip"
        )
    
    def get_logger(self):
        """Get configured logger instance"""
        return logger.bind(name=self.name)


# Create default logger instance
log = CustomLogger().get_logger()
