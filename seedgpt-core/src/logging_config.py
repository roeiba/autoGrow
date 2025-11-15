"""
Centralized logging configuration for the AI Project Template.

Provides structured logging with:
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- File rotation to prevent disk space issues
- JSON formatting for production environments
- Console output for development
- Performance tracking
- Error tracking with context
"""

import logging
import logging.handlers
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import os


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    Outputs logs in JSON format for easy parsing and analysis.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, "extra_data"):
            log_data["extra"] = record.extra_data

        # Add performance metrics if present
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms

        # Add request/operation context
        if hasattr(record, "operation"):
            log_data["operation"] = record.operation

        if hasattr(record, "status"):
            log_data["status"] = record.status

        return json.dumps(log_data)


class ColoredConsoleFormatter(logging.Formatter):
    """
    Colored console formatter for better readability in development.
    """

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]

        # Format: [TIMESTAMP] LEVEL - MODULE.FUNCTION:LINE - MESSAGE
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        location = f"{record.module}.{record.funcName}:{record.lineno}"

        formatted = (
            f"{color}[{timestamp}] {record.levelname:8s}{reset} - "
            f"{location:30s} - {record.getMessage()}"
        )

        # Add exception info if present
        if record.exc_info:
            formatted += f"\n{self.formatException(record.exc_info)}"

        return formatted


def setup_logging(
    name: str = "ai_project",
    level: str = "INFO",
    log_dir: Optional[Path] = None,
    console: bool = True,
    json_format: bool = False,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Set up logging configuration.

    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (None = no file logging)
        console: Enable console output
        json_format: Use JSON format (for production)
        max_bytes: Max size per log file before rotation
        backup_count: Number of backup files to keep

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logging("my_app", level="DEBUG")
        >>> logger.info("Application started")
        >>> logger.error("An error occurred", exc_info=True)
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))

        if json_format:
            console_handler.setFormatter(JSONFormatter())
        else:
            console_handler.setFormatter(ColoredConsoleFormatter())

        logger.addHandler(console_handler)

    # File handler with rotation
    if log_dir:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        # Main log file
        log_file = log_dir / f"{name}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setLevel(getattr(logging, level.upper()))

        if json_format:
            file_handler.setFormatter(JSONFormatter())
        else:
            # Use standard format for file logs
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - "
                "%(module)s.%(funcName)s:%(lineno)d - %(message)s"
            )
            file_handler.setFormatter(file_formatter)

        logger.addHandler(file_handler)

        # Separate error log file
        error_log_file = log_dir / f"{name}_errors.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        error_handler.setLevel(logging.ERROR)

        if json_format:
            error_handler.setFormatter(JSONFormatter())
        else:
            error_handler.setFormatter(file_formatter)

        logger.addHandler(error_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the project's configuration.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing started")
    """
    # Check environment for configuration
    level = os.getenv("LOG_LEVEL", "INFO")
    json_format = os.getenv("LOG_FORMAT", "console") == "json"
    log_dir = os.getenv("LOG_DIR")

    if log_dir:
        log_dir = Path(log_dir)

    return setup_logging(
        name=name, level=level, log_dir=log_dir, console=True, json_format=json_format
    )


class LogContext:
    """
    Context manager for adding extra context to logs.

    Example:
        >>> logger = get_logger(__name__)
        >>> with LogContext(logger, operation="api_call", user_id=123):
        ...     logger.info("Making API call")
        ...     # Logs will include operation and user_id
    """

    def __init__(self, logger: logging.Logger, **context):
        self.logger = logger
        self.context = context
        self.old_factory = None

    def __enter__(self):
        """Add context to logger."""
        self.old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            for key, value in self.context.items():
                setattr(record, key, value)
            return record

        logging.setLogRecordFactory(record_factory)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore original factory."""
        if self.old_factory:
            logging.setLogRecordFactory(self.old_factory)


def log_performance(logger: logging.Logger, operation: str):
    """
    Decorator to log function performance.

    Args:
        logger: Logger instance
        operation: Operation name for logging

    Example:
        >>> logger = get_logger(__name__)
        >>> @log_performance(logger, "data_processing")
        ... def process_data(data):
        ...     # Process data
        ...     return result
    """
    import time
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logger.info(f"Starting {operation}: {func.__name__}")

            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000

                # Log with performance metrics
                extra = logging.LogRecord(
                    name=logger.name,
                    level=logging.INFO,
                    pathname="",
                    lineno=0,
                    msg=f"Completed {operation}: {func.__name__}",
                    args=(),
                    exc_info=None,
                )
                extra.duration_ms = duration_ms
                extra.operation = operation
                extra.status = "success"

                logger.handle(extra)

                return result

            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000

                # Log with error context
                extra = logging.LogRecord(
                    name=logger.name,
                    level=logging.ERROR,
                    pathname="",
                    lineno=0,
                    msg=f"Failed {operation}: {func.__name__} - {str(e)}",
                    args=(),
                    exc_info=sys.exc_info(),
                )
                extra.duration_ms = duration_ms
                extra.operation = operation
                extra.status = "error"

                logger.handle(extra)
                raise

        return wrapper

    return decorator


# Default logger for the project
default_logger = get_logger("ai_project")


if __name__ == "__main__":
    # Example usage
    logger = setup_logging(
        name="example",
        level="DEBUG",
        log_dir=Path("logs"),
        console=True,
        json_format=False,
    )

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    try:
        raise ValueError("Example error")
    except Exception:
        logger.exception("An exception occurred")

    # With context
    with LogContext(logger, operation="test", user_id=123):
        logger.info("Message with context")

    # With performance logging
    @log_performance(logger, "test_operation")
    def slow_function():
        import time

        time.sleep(0.1)
        return "done"

    result = slow_function()
    logger.info(f"Result: {result}")
