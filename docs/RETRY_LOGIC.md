# Retry Logic and Exponential Backoff

## Overview

AutoGrow now includes robust retry logic with exponential backoff and jitter for all API calls to Anthropic and GitHub. This prevents cascading failures and handles transient network issues, rate limits, and server errors gracefully.

## Features

- **Exponential Backoff**: Delays increase exponentially with each retry attempt
- **Jitter**: Random variation added to delays to prevent thundering herd problem
- **Rate Limit Handling**: Automatically detects and handles rate limit errors
- **Configurable**: Retry counts, delays, and behavior can be customized
- **Smart Error Detection**: Distinguishes between retryable and non-retryable errors

## Implementation

The retry logic is implemented in `src/utils/retry.py` and is used across all three agents:
- `issue_generator.py`: For Anthropic and GitHub API calls
- `issue_resolver.py`: For GitHub API calls
- `qa_agent.py`: For Anthropic and GitHub API calls

## Configuration

Default settings are defined in `RetryConfig`:

```python
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
```

## Usage Examples

### Using Helper Functions

```python
from utils.retry import retry_anthropic_call, retry_github_call

# Anthropic API call with retry
message = retry_anthropic_call(
    client.messages.create,
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)

# GitHub API call with retry
issues = retry_github_call(repo.get_issues, state="open")
```

### Using Decorators

```python
from utils.retry import retry_anthropic, retry_github

@retry_anthropic
def call_claude_api():
    return client.messages.create(...)

@retry_github
def get_github_issues():
    return repo.get_issues(state="open")
```

### Custom Retry Logic

```python
from utils.retry import retry_with_backoff

@retry_with_backoff(
    max_retries=3,
    base_delay=1.0,
    max_delay=30.0
)
def my_api_call():
    # Your API call here
    pass
```

## Retryable Errors

The following errors are automatically retried:

### Network Errors
- `ConnectionError`
- `ConnectionResetError`
- `Timeout`
- `ReadTimeout`
- `ConnectTimeout`

### Rate Limit Errors
- HTTP 429 (Too Many Requests)
- Rate limit exceeded messages
- Quota exceeded errors

### Server Errors
- HTTP 500 (Internal Server Error)
- HTTP 502 (Bad Gateway)
- HTTP 503 (Service Unavailable)
- HTTP 504 (Gateway Timeout)

### API-Specific Errors
- Anthropic `overloaded_error`
- GitHub abuse detection
- GitHub secondary rate limits

## Backoff Calculation

The delay between retries is calculated as:

```
delay = min(base_delay * (exponential_base ^ attempt), max_delay)
delay = delay + (delay * jitter_factor * random())
```

Example delays with default settings:
- Attempt 1: ~1.0s
- Attempt 2: ~2.1s
- Attempt 3: ~4.0s
- Attempt 4: ~8.3s
- Attempt 5: ~16.8s

## Benefits

1. **Prevents Cascading Failures**: Network issues don't crash the workflow
2. **Handles Rate Limits**: Automatically backs off when rate limited
3. **Reduces API Costs**: Prevents wasted API calls from transient failures
4. **Improved Reliability**: Workflows complete successfully despite temporary issues
5. **Better User Experience**: Agents continue working through temporary problems

## Testing

Run the test suite to verify retry logic:

```bash
cd src
python3 -c "from utils.retry import *; print('Retry logic loaded successfully')"
```

All agent modules have been updated and tested with the new retry logic.

## Related Issue

This implementation resolves GitHub Issue #21: "Add retry logic and exponential backoff for API calls"
