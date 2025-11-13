# Retry Logic with Tenacity

## Overview

AutoGrow uses [Tenacity](https://pypi.org/project/tenacity/), a robust and battle-tested Python retry library, to handle transient failures in API calls to GitHub and Anthropic (Claude AI). This ensures reliability in the face of network issues, rate limits, and temporary service disruptions.

## Why Tenacity?

Tenacity provides several advantages over custom retry implementations:

- **Proven Reliability**: Used by thousands of projects with extensive testing
- **Flexible Configuration**: Multiple retry strategies, stop conditions, and wait strategies
- **Comprehensive Logging**: Built-in logging support for debugging and monitoring
- **Jitter Support**: Automatic jitter to prevent thundering herd problems
- **Clean API**: Decorator-based interface that's easy to use and understand
- **Active Maintenance**: Regularly updated with bug fixes and improvements

## Installation

Tenacity is automatically installed as part of AutoGrow's dependencies:

```bash
pip install tenacity>=8.2.0
```

It's included in both:
- `tests/requirements.txt`
- `src/claude-agent/requirements.txt`

## Usage

### Basic Usage

The `src/utils/retry.py` module provides pre-configured decorators for common use cases:

#### Retry GitHub API Calls

```python
from utils.retry import retry_github_api

@retry_github_api
def create_github_issue():
    return repo.create_issue(title="Bug", body="Description")
```

**Configuration:**
- **Max Retries**: 3 attempts (initial + 2 retries)
- **Backoff**: Exponential with base 2 (2s, 4s, 8s)
- **Max Delay**: 120 seconds
- **Jitter**: Enabled by default
- **Retries On**: Rate limits (403), network errors, timeouts, 500/502/503 errors

#### Retry Anthropic API Calls

```python
from utils.retry import retry_anthropic_api

@retry_anthropic_api
def call_claude():
    return client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": "Hello"}]
    )
```

**Configuration:**
- **Max Retries**: 5 attempts (initial + 4 retries)
- **Backoff**: Exponential with base 2 (1s, 2s, 4s, 8s, 16s)
- **Max Delay**: 60 seconds
- **Jitter**: Enabled by default
- **Retries On**: Rate limits (429), network errors, timeouts, 502/503 errors

### Custom Retry Configuration

For custom retry behavior, use the `retry_with_backoff` decorator:

```python
from utils.retry import retry_with_backoff, RetryConfig

@retry_with_backoff(
    config=RetryConfig(
        max_retries=3,
        base_delay=1.0,
        max_delay=30.0,
        exponential_base=2.0,
        jitter=True
    ),
    retryable_exceptions=(ConnectionError, TimeoutError)
)
def my_api_call():
    # Your API call here
    pass
```

### Exception Classification

The retry module automatically classifies exceptions to determine if they should be retried:

#### Retryable Exceptions

These exceptions will trigger a retry:

1. **Custom Exception Classes**:
   - `RetryableError` - Base class for retryable errors
   - `RateLimitError` - Rate limit exceeded (429, 403 for GitHub)
   - `NetworkError` - Network-related failures

2. **Built-in Exceptions**:
   - `ConnectionError`
   - `TimeoutError`

3. **Exception Message Indicators**:
   - "timeout", "timed out"
   - "connection", "network"
   - "temporary", "unavailable"
   - "503", "502", "429"
   - "rate limit", "too many requests"

#### Non-Retryable Exceptions

These will fail immediately without retry:

- `ValueError` - Invalid input parameters
- `KeyError` - Missing required data
- `AuthenticationError` - Invalid credentials
- Any exception not matching the retryable criteria above

## How It Works

### Exponential Backoff with Jitter

AutoGrow uses exponential backoff to progressively increase the wait time between retries:

```
Attempt 1: Initial call
Attempt 2: Wait ~2 seconds (with jitter)
Attempt 3: Wait ~4 seconds (with jitter)
Attempt 4: Wait ~8 seconds (with jitter)
...
```

**Jitter** adds randomness (±25%) to prevent multiple clients from retrying simultaneously (thundering herd problem).

### Rate Limit Handling

When a rate limit error is detected:

1. The error is classified as `RateLimitError`
2. If the API provides a `Retry-After` header, that value is used
3. Otherwise, exponential backoff is applied
4. The retry waits for the appropriate duration before attempting again

### Logging

Tenacity provides detailed logging for all retry attempts:

```
WARNING:utils.retry:Retrying in 2.0 seconds after attempt 1 of 4 (github.GithubException: 403 Rate limit exceeded)
WARNING:utils.retry:Retrying in 4.0 seconds after attempt 2 of 4 (github.GithubException: 403 Rate limit exceeded)
```

To adjust logging verbosity, configure the logger:

```python
import logging
logging.getLogger('utils.retry').setLevel(logging.DEBUG)
```

## Integration Points

The retry logic is integrated throughout AutoGrow:

### GitHub Actions Scripts

All GitHub Actions wrapper scripts use retry logic:

- `.github/scripts/issue_generator.py` - Issue generation
- `.github/scripts/issue_resolver.py` - Issue resolution
- `.github/scripts/qa_agent.py` - Quality assurance

### Core Agent Modules

The retry decorators are applied to:

- `src/agents/issue_generator.py` - Creating issues
- `src/agents/issue_resolver.py` - Resolving issues and creating PRs
- `src/agents/qa_agent.py` - Running QA checks

### Example from Issue Generator

```python
@retry_github_api
def get_open_issues():
    return list(self.repo.get_issues(state="open"))

@retry_github_api
def create_issue():
    return self.repo.create_issue(
        title=title,
        body=full_body,
        labels=labels
    )

@retry_anthropic_api
def call_anthropic():
    client = Anthropic(api_key=self.anthropic_api_key)
    return client.messages.create(
        model=CLAUDE_MODELS.ISSUE_GENERATION,
        max_tokens=CLAUDE_MODELS.DEFAULT_MAX_TOKENS,
        system=SystemPrompts.ISSUE_GENERATOR,
        messages=[{"role": "user", "content": prompt}],
    )
```

## Best Practices

### 1. Use Specific Decorators

Prefer `@retry_github_api` and `@retry_anthropic_api` over generic retry decorators:

```python
# Good
@retry_github_api
def create_pr():
    return repo.create_pull(...)

# Less optimal
@retry_with_backoff(config=RetryConfig(...))
def create_pr():
    return repo.create_pull(...)
```

### 2. Wrap Individual Operations

Apply retry decorators to individual API operations rather than large functions:

```python
# Good - Specific operation
@retry_github_api
def get_issues():
    return repo.get_issues(state="open")

# Avoid - Too broad
@retry_github_api
def process_all_issues():
    issues = get_issues()
    for issue in issues:
        process_issue(issue)  # This shouldn't be retried
```

### 3. Let Non-Retryable Errors Fail Fast

Don't catch and suppress exceptions that shouldn't be retried:

```python
# Good
@retry_github_api
def validate_and_create():
    if not valid_input:
        raise ValueError("Invalid input")  # Fails immediately
    return repo.create_issue(...)

# Avoid
@retry_github_api
def validate_and_create():
    try:
        if not valid_input:
            raise ValueError("Invalid input")
        return repo.create_issue(...)
    except Exception:
        return None  # Suppresses retryable errors!
```

### 4. Monitor Retry Logs

In production, monitor retry logs to identify:
- Frequent rate limiting (may need to reduce request rate)
- Network issues (may need infrastructure improvements)
- API instability (may need to contact service provider)

## Testing

### Unit Tests

Test retry behavior with mock failures:

```python
from unittest.mock import Mock, patch
from utils.retry import retry_github_api

def test_retry_on_network_error():
    mock_func = Mock(side_effect=[
        ConnectionError("Network error"),
        ConnectionError("Network error"),
        "Success"
    ])

    @retry_github_api
    def call_api():
        return mock_func()

    result = call_api()
    assert result == "Success"
    assert mock_func.call_count == 3
```

### Integration Tests

Test actual retry behavior with rate limit scenarios:

```bash
# Run tests that exercise retry logic
python -m pytest tests/integration/test_retry_behavior.py -v
```

## Troubleshooting

### Issue: Retries Not Working

**Symptoms**: Failures happen without retries

**Solutions**:
1. Check that the exception is retryable (see Exception Classification above)
2. Verify the decorator is applied: `@retry_github_api` or `@retry_anthropic_api`
3. Check logs for retry attempts
4. Ensure Tenacity is installed: `pip install tenacity>=8.2.0`

### Issue: Too Many Retries

**Symptoms**: Operations take too long due to excessive retries

**Solutions**:
1. Reduce `max_retries` in custom `RetryConfig`
2. Check if the API is consistently failing (may need different approach)
3. Verify network connectivity and API status

### Issue: Rate Limits Still Occurring

**Symptoms**: Rate limit errors despite retry logic

**Solutions**:
1. The retry logic will eventually exhaust attempts if rate limits persist
2. Consider implementing request throttling before the API call
3. Check if you're within API rate limits (GitHub: 5000/hour for authenticated)
4. Implement exponential backoff at the application level, not just retries

## Advanced Usage

### Custom Wait Strategy

For specialized retry patterns:

```python
from tenacity import retry, wait_fixed, stop_after_attempt

@retry(
    wait=wait_fixed(5),  # Fixed 5-second wait
    stop=stop_after_attempt(3),
    reraise=True
)
def custom_retry_function():
    # Your code here
    pass
```

### Conditional Retry

Retry based on return values:

```python
from tenacity import retry, retry_if_result

def is_rate_limited(result):
    return result.status_code == 429

@retry(retry=retry_if_result(is_rate_limited))
def api_call():
    return requests.get("https://api.example.com")
```

### Retry Callbacks

Execute code before/after retry attempts:

```python
from tenacity import retry, before_log, after_log
import logging

logger = logging.getLogger(__name__)

@retry(
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.INFO)
)
def monitored_api_call():
    # Your code here
    pass
```

## References

- [Tenacity Documentation](https://tenacity.readthedocs.io/)
- [Tenacity PyPI](https://pypi.org/project/tenacity/)
- [GitHub API Rate Limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- [Anthropic API Documentation](https://docs.anthropic.com/)

## Migration Notes

This module was migrated from a custom retry implementation to Tenacity in issue #31. The migration maintains backward compatibility with existing code while providing:

- More robust retry logic
- Better logging and debugging
- Proven reliability at scale
- Active maintenance and community support

All existing decorators (`@retry_github_api`, `@retry_anthropic_api`, `retry_with_backoff`) work exactly as before, with improved reliability under the hood.
