#!/usr/bin/env python3
"""
Retry utility with exponential backoff and jitter for API calls.

Provides robust retry logic for Anthropic API and GitHub API calls with:
- Exponential backoff
- Jitter to prevent thundering herd
- Rate limit handling
- Configurable retry attempts
- Detailed error logging
"""

import time
import random
import logging
from typing import Callable, TypeVar, Optional, Any
from functools import wraps

# Setup logger
logger = logging.getLogger(__name__)

T = TypeVar('T')


class RetryConfig:
    """Configuration for retry behavior"""

    # Default retry settings
    MAX_RETRIES = 5
    BASE_DELAY = 1.0  # seconds
    MAX_DELAY = 60.0  # seconds
    EXPONENTIAL_BASE = 2
    JITTER_FACTOR = 0.1  # 10% jitter

    # API-specific settings
    ANTHROPIC_MAX_RETRIES = 5
    ANTHROPIC_BASE_DELAY = 2.0
    GITHUB_MAX_RETRIES = 5
    GITHUB_BASE_DELAY = 1.0

    # Rate limit retry settings
    RATE_LIMIT_MAX_RETRIES = 3
    RATE_LIMIT_BASE_DELAY = 5.0


class RetryError(Exception):
    """Exception raised when all retry attempts are exhausted"""
    pass


def calculate_backoff_delay(
    attempt: int,
    base_delay: float = RetryConfig.BASE_DELAY,
    max_delay: float = RetryConfig.MAX_DELAY,
    exponential_base: float = RetryConfig.EXPONENTIAL_BASE,
    jitter_factor: float = RetryConfig.JITTER_FACTOR
) -> float:
    """
    Calculate delay with exponential backoff and jitter.

    Args:
        attempt: Current attempt number (0-indexed)
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential calculation
        jitter_factor: Jitter factor (0.0 to 1.0)

    Returns:
        Delay in seconds with jitter applied
    """
    # Calculate exponential backoff
    delay = min(base_delay * (exponential_base ** attempt), max_delay)

    # Add jitter to prevent thundering herd
    jitter = delay * jitter_factor * random.random()

    return delay + jitter


def is_retryable_error(exception: Exception) -> bool:
    """
    Determine if an error is retryable.

    Args:
        exception: The exception to check

    Returns:
        True if the error is retryable, False otherwise
    """
    # Convert exception to string for checking
    error_str = str(exception).lower()
    error_type = type(exception).__name__

    # Network/connection errors - always retry
    retryable_types = [
        'ConnectionError',
        'ConnectionResetError',
        'Timeout',
        'TimeoutError',
        'ReadTimeout',
        'ConnectTimeout',
        'HTTPError',
    ]

    if error_type in retryable_types:
        return True

    # Rate limit errors - retry with backoff
    rate_limit_indicators = [
        'rate limit',
        'ratelimit',
        'too many requests',
        '429',
        'quota exceeded',
    ]

    if any(indicator in error_str for indicator in rate_limit_indicators):
        return True

    # Temporary server errors - retry
    server_error_indicators = [
        '500',
        '502',
        '503',
        '504',
        'internal server error',
        'bad gateway',
        'service unavailable',
        'gateway timeout',
        'overloaded',
    ]

    if any(indicator in error_str for indicator in server_error_indicators):
        return True

    # Anthropic-specific errors
    anthropic_retryable = [
        'overloaded_error',
        'api_error',
    ]

    if any(indicator in error_str for indicator in anthropic_retryable):
        return True

    # GitHub-specific errors
    github_retryable = [
        'abuse detection',
        'secondary rate limit',
    ]

    if any(indicator in error_str for indicator in github_retryable):
        return True

    return False


def retry_with_backoff(
    max_retries: int = RetryConfig.MAX_RETRIES,
    base_delay: float = RetryConfig.BASE_DELAY,
    max_delay: float = RetryConfig.MAX_DELAY,
    exponential_base: float = RetryConfig.EXPONENTIAL_BASE,
    jitter_factor: float = RetryConfig.JITTER_FACTOR,
    on_retry: Optional[Callable[[Exception, int], None]] = None
):
    """
    Decorator for retrying functions with exponential backoff and jitter.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential calculation
        jitter_factor: Jitter factor (0.0 to 1.0)
        on_retry: Optional callback function called on each retry

    Returns:
        Decorated function with retry logic

    Example:
        @retry_with_backoff(max_retries=3, base_delay=2.0)
        def call_api():
            return api.request()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    last_exception = e

                    # Check if we should retry
                    if attempt >= max_retries:
                        logger.error(
                            f"All {max_retries} retry attempts exhausted for {func.__name__}. "
                            f"Last error: {e}"
                        )
                        raise RetryError(
                            f"Failed after {max_retries} retries: {e}"
                        ) from e

                    if not is_retryable_error(e):
                        logger.warning(
                            f"Non-retryable error in {func.__name__}: {e}"
                        )
                        raise

                    # Calculate delay
                    delay = calculate_backoff_delay(
                        attempt,
                        base_delay=base_delay,
                        max_delay=max_delay,
                        exponential_base=exponential_base,
                        jitter_factor=jitter_factor
                    )

                    logger.warning(
                        f"Retry attempt {attempt + 1}/{max_retries} for {func.__name__} "
                        f"after error: {e}. Waiting {delay:.2f}s before retry..."
                    )

                    # Call retry callback if provided
                    if on_retry:
                        on_retry(e, attempt + 1)

                    # Wait before retry
                    time.sleep(delay)

            # This should never be reached, but just in case
            raise last_exception

        return wrapper
    return decorator


def retry_anthropic_call(
    func: Callable[..., T],
    *args,
    max_retries: int = RetryConfig.ANTHROPIC_MAX_RETRIES,
    base_delay: float = RetryConfig.ANTHROPIC_BASE_DELAY,
    **kwargs
) -> T:
    """
    Helper function to retry Anthropic API calls with appropriate defaults.

    Args:
        func: Function to retry
        *args: Positional arguments for the function
        max_retries: Maximum number of retries
        base_delay: Base delay between retries
        **kwargs: Keyword arguments for the function

    Returns:
        Result of the function call

    Example:
        result = retry_anthropic_call(
            client.messages.create,
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}]
        )
    """
    @retry_with_backoff(
        max_retries=max_retries,
        base_delay=base_delay,
        on_retry=lambda e, attempt: logger.info(
            f"Anthropic API retry {attempt}/{max_retries}: {e}"
        )
    )
    def _wrapped_call():
        return func(*args, **kwargs)

    return _wrapped_call()


def retry_github_call(
    func: Callable[..., T],
    *args,
    max_retries: int = RetryConfig.GITHUB_MAX_RETRIES,
    base_delay: float = RetryConfig.GITHUB_BASE_DELAY,
    **kwargs
) -> T:
    """
    Helper function to retry GitHub API calls with appropriate defaults.

    Args:
        func: Function to retry
        *args: Positional arguments for the function
        max_retries: Maximum number of retries
        base_delay: Base delay between retries
        **kwargs: Keyword arguments for the function

    Returns:
        Result of the function call

    Example:
        issues = retry_github_call(repo.get_issues, state="open")
    """
    @retry_with_backoff(
        max_retries=max_retries,
        base_delay=base_delay,
        on_retry=lambda e, attempt: logger.info(
            f"GitHub API retry {attempt}/{max_retries}: {e}"
        )
    )
    def _wrapped_call():
        return func(*args, **kwargs)

    return _wrapped_call()


# Convenience decorators with pre-configured settings
def retry_anthropic(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator for Anthropic API calls with default retry settings.

    Example:
        @retry_anthropic
        def call_claude_api():
            return client.messages.create(...)
    """
    return retry_with_backoff(
        max_retries=RetryConfig.ANTHROPIC_MAX_RETRIES,
        base_delay=RetryConfig.ANTHROPIC_BASE_DELAY
    )(func)


def retry_github(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator for GitHub API calls with default retry settings.

    Example:
        @retry_github
        def get_github_issues():
            return repo.get_issues(state="open")
    """
    return retry_with_backoff(
        max_retries=RetryConfig.GITHUB_MAX_RETRIES,
        base_delay=RetryConfig.GITHUB_BASE_DELAY
    )(func)
