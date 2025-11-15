# Error Handling Improvements

## Overview
Improved error handling for Claude CLI credit balance issues and other API errors to provide clear, actionable error messages.

## Changes Made

### 1. New Exception Type: `CreditBalanceError`
**File**: `src/utils/exceptions.py`

Added a new exception class specifically for handling credit balance and quota issues:

```python
class CreditBalanceError(APIError):
    """Raised when API credit balance is too low or quota exceeded."""
    
    def __init__(self, service: str, message: str = None):
        default_msg = f"{service} credit balance is too low or quota exceeded"
        super().__init__(
            message or default_msg,
            details={"service": service}
        )
        self.service = service
```

### 2. Enhanced Claude CLI Error Detection
**File**: `src/claude-agent/claude_cli_agent.py`

Improved error detection in both streaming and non-streaming modes to identify specific error types:

- **Credit Balance Issues**: Detects "credit balance is too low" or "quota" in stdout
- **Authentication Issues**: Detects "authentication", "unauthorized", or "api key" in stdout
- **Generic Errors**: Falls back to standard error handling

**Before**:
```
Claude CLI error (exit code 1): No error message provided
Stdout: Credit balance is too low
```

**After**:
```
Claude CLI credit balance is too low: Credit balance is too low
```

### 3. Improved Error Conversion
**File**: `src/utils/exceptions.py`

Enhanced `get_exception_for_anthropic_error()` to handle `AgentError` from Claude CLI:

```python
def get_exception_for_anthropic_error(error, default_message: str = None):
    # Handle AgentError from Claude CLI
    if isinstance(error, AgentError):
        error_str = str(error).lower()
        
        # Check for credit balance issues
        if 'credit balance is too low' in error_str or 'quota' in error_str:
            return CreditBalanceError('Claude CLI', message=str(error))
        
        # Check for authentication issues
        if 'authentication' in error_str or 'unauthorized' in error_str:
            return AuthenticationError(f"Claude CLI authentication failed: {error}")
        
        # Return as generic AnthropicAPIError with details
        ...
```

### 4. Comprehensive Error Handling in Workflow Scripts
**Files**: 
- `.github/scripts/issue_generator.py`
- `.github/scripts/issue_resolver.py`

Added specific exception handlers for all error types:

```python
except CreditBalanceError as e:
    logger.error(
        "❌ Claude CLI credit balance is too low. Please add credits to your Claude account.",
        extra={"error_details": e.details}
    )
    sys.exit(1)

except RateLimitError as e:
    logger.error(f"❌ {e.service} API rate limit exceeded.")
    sys.exit(1)

except AuthenticationError as e:
    logger.error("❌ Authentication failed. Please check your API credentials.")
    sys.exit(1)

except AnthropicAPIError as e:
    logger.error("❌ Claude API error occurred.")
    sys.exit(1)

except GitHubAPIError as e:
    logger.error("❌ GitHub API error occurred.")
    sys.exit(1)
```

## Error Flow

### Original Flow (Problematic)
```
Claude CLI → stdout: "Credit balance is too low" (exit code 1)
    ↓
claude_cli_agent.py → AgentError("Claude CLI error (exit code 1): No error message provided\nStdout: Credit balance is too low")
    ↓
issue_generator.py → get_exception_for_anthropic_error(AgentError)
    ↓
AnthropicAPIError("Failed to call Claude API") ← Lost the actual error!
```

### New Flow (Fixed)
```
Claude CLI → stdout: "Credit balance is too low" (exit code 1)
    ↓
claude_cli_agent.py → AgentError("Claude CLI credit balance is too low: Credit balance is too low")
    ↓
issue_generator.py → get_exception_for_anthropic_error(AgentError)
    ↓
CreditBalanceError("Claude CLI credit balance is too low: Credit balance is too low")
    ↓
.github/scripts/issue_generator.py → Clear error message with actionable advice
```

## Benefits

1. **Clear Error Messages**: Users immediately understand what went wrong
2. **Actionable Advice**: Error messages include guidance on how to fix the issue
3. **Proper Error Types**: Each error type has its own exception class
4. **Structured Logging**: Error details are logged with proper context
5. **Exit Codes**: Proper exit codes for CI/CD workflows

## Testing

A test script was created to verify the error handling:

```bash
python3 .agents/scripts/test_credit_error.py
```

**Output**:
```
✅ Credit balance error correctly detected!
  Service: Claude CLI
```

## Example Error Messages

### Credit Balance Error
```
[2025-11-14 12:00:00] ERROR - ❌ Claude CLI credit balance is too low. Please add credits to your Claude account.
[2025-11-14 12:00:00] ERROR - Error: Claude CLI credit balance is too low: Credit balance is too low
```

### Rate Limit Error
```
[2025-11-14 12:00:00] ERROR - ❌ Anthropic API rate limit exceeded.
[2025-11-14 12:00:00] ERROR - Please retry after: 1731585600
```

### Authentication Error
```
[2025-11-14 12:00:00] ERROR - ❌ Authentication failed. Please check your API credentials.
```

## Future Improvements

1. Add retry logic for rate limit errors with exponential backoff
2. Implement automatic fallback from Claude CLI to Anthropic SDK on credit errors
3. Add monitoring/alerting for credit balance thresholds
4. Create a dashboard for tracking API usage and errors
