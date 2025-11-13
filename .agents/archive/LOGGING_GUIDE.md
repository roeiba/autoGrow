# Production Logging Guide

Complete guide for implementing professional logging throughout the AI Project Template.

## 📋 Overview

This project uses a centralized logging system with:
- **Structured logging** (JSON format for production)
- **Multiple log levels** (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **File rotation** (prevents disk space issues)
- **Colored console output** (for development)
- **Performance tracking** (automatic timing)
- **Error tracking** (with full context)

## 🚀 Quick Start

### Basic Usage

```python
from logging_config import get_logger

# Get logger for your module
logger = get_logger(__name__)

# Log at different levels
logger.debug("Detailed debugging information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical system error")

# Log with exception info
try:
    risky_operation()
except Exception as e:
    logger.exception("Operation failed")  # Includes full traceback
```

### Configuration via Environment Variables

```bash
# Set log level
export LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Set log format
export LOG_FORMAT=json  # json or console

# Set log directory
export LOG_DIR=./logs
```

## 📝 Logging Patterns

### 1. Function Entry/Exit

```python
def process_data(data):
    logger.info(f"Processing data: {len(data)} items")
    
    try:
        result = perform_processing(data)
        logger.info(f"Processing completed: {len(result)} results")
        return result
    except Exception as e:
        logger.error(f"Processing failed: {e}", exc_info=True)
        raise
```

### 2. Performance Logging

```python
from logging_config import log_performance

@log_performance(logger, "data_processing")
def process_large_dataset(data):
    # Function automatically logs:
    # - Start time
    # - End time
    # - Duration in milliseconds
    # - Success/failure status
    return processed_data
```

### 3. Context Logging

```python
from logging_config import LogContext

# Add context to all logs within the block
with LogContext(logger, operation="api_call", user_id=123, request_id="abc"):
    logger.info("Starting API call")
    # Logs will include: operation, user_id, request_id
    result = make_api_call()
    logger.info("API call completed")
```

### 4. API Call Logging

```python
def query_gemini_api(prompt):
    logger.info(f"Gemini API call started", extra={
        "prompt_length": len(prompt),
        "model": self.model
    })
    
    try:
        result = self._make_request(prompt)
        
        logger.info("Gemini API call succeeded", extra={
            "response_length": len(result),
            "tokens_used": result.get("usage", {}).get("total_tokens")
        })
        
        return result
    
    except Exception as e:
        logger.error(f"Gemini API call failed: {e}", extra={
            "prompt_length": len(prompt),
            "error_type": type(e).__name__
        }, exc_info=True)
        raise
```

### 5. Batch Operation Logging

```python
def batch_process(files):
    logger.info(f"Starting batch process: {len(files)} files")
    
    results = []
    errors = 0
    
    for i, file in enumerate(files):
        try:
            logger.debug(f"Processing file {i+1}/{len(files)}: {file}")
            result = process_file(file)
            results.append(result)
        except Exception as e:
            errors += 1
            logger.warning(f"File processing failed: {file}", exc_info=True)
    
    logger.info(f"Batch process completed: {len(results)} succeeded, {errors} failed")
    return results
```

### 6. Test Logging

```python
import pytest
from logging_config import get_logger

logger = get_logger(__name__)

def test_integration():
    logger.info("Starting integration test")
    
    try:
        result = run_test()
        logger.info(f"Test passed: {result}")
        assert result is not None
    except AssertionError as e:
        logger.error(f"Test failed: {e}")
        raise
```

## 🎯 Logging Best Practices

### DO ✅

1. **Log at appropriate levels**
   ```python
   logger.debug("Variable value: x=5")          # Debugging details
   logger.info("User logged in: user_id=123")   # Normal operations
   logger.warning("API rate limit approaching")  # Potential issues
   logger.error("Database connection failed")    # Errors
   logger.critical("System out of memory")       # Critical failures
   ```

2. **Include context**
   ```python
   logger.info("Processing request", extra={
       "user_id": user_id,
       "request_id": request_id,
       "endpoint": endpoint
   })
   ```

3. **Log exceptions with traceback**
   ```python
   try:
       risky_operation()
   except Exception as e:
       logger.exception("Operation failed")  # Includes full traceback
   ```

4. **Use structured data**
   ```python
   logger.info("API call completed", extra={
       "duration_ms": 150,
       "status_code": 200,
       "tokens_used": 1500
   })
   ```

5. **Log performance metrics**
   ```python
   import time
   start = time.time()
   result = expensive_operation()
   duration = (time.time() - start) * 1000
   logger.info(f"Operation completed in {duration:.2f}ms")
   ```

### DON'T ❌

1. **Don't log sensitive data**
   ```python
   # ❌ BAD
   logger.info(f"API key: {api_key}")
   logger.info(f"Password: {password}")
   
   # ✅ GOOD
   logger.info(f"API key configured (length: {len(api_key)})")
   logger.info("User authenticated successfully")
   ```

2. **Don't log in tight loops**
   ```python
   # ❌ BAD
   for item in large_list:
       logger.info(f"Processing {item}")  # Too many logs!
   
   # ✅ GOOD
   logger.info(f"Processing {len(large_list)} items")
   for item in large_list:
       process(item)
   logger.info("Processing completed")
   ```

3. **Don't use print statements**
   ```python
   # ❌ BAD
   print("Starting process")
   
   # ✅ GOOD
   logger.info("Starting process")
   ```

4. **Don't log without context**
   ```python
   # ❌ BAD
   logger.error("Failed")
   
   # ✅ GOOD
   logger.error("API call failed: timeout after 30s", extra={
       "endpoint": "/api/v1/query",
       "timeout_seconds": 30
   })
   ```

5. **Don't ignore log levels**
   ```python
   # ❌ BAD
   logger.info("x=5, y=10, z=15")  # Debug info at INFO level
   
   # ✅ GOOD
   logger.debug("x=5, y=10, z=15")  # Use DEBUG for details
   ```

## 📊 Log Levels Guide

| Level | When to Use | Example |
|-------|-------------|---------|
| **DEBUG** | Detailed diagnostic info | Variable values, function calls |
| **INFO** | General informational messages | Process started, request received |
| **WARNING** | Potentially harmful situations | Deprecated API used, rate limit approaching |
| **ERROR** | Error events that might still allow the app to continue | API call failed, file not found |
| **CRITICAL** | Very severe error events that might cause the app to abort | Out of memory, database unavailable |

## 🔧 Configuration Examples

### Development (Console, Colored, DEBUG)

```python
from logging_config import setup_logging

logger = setup_logging(
    name="my_app",
    level="DEBUG",
    console=True,
    json_format=False
)
```

### Production (JSON, File, INFO)

```python
from logging_config import setup_logging
from pathlib import Path

logger = setup_logging(
    name="my_app",
    level="INFO",
    log_dir=Path("/var/log/my_app"),
    console=True,
    json_format=True
)
```

### Testing (Console only, WARNING)

```python
from logging_config import setup_logging

logger = setup_logging(
    name="test",
    level="WARNING",
    console=True,
    json_format=False
)
```

## 📁 Log File Structure

When file logging is enabled:

```
logs/
├── ai_project.log          # Main log file (all levels)
├── ai_project.log.1        # Rotated backup 1
├── ai_project.log.2        # Rotated backup 2
├── ai_project_errors.log   # Error log (ERROR+ only)
├── ai_project_errors.log.1 # Error backup 1
└── ai_project_errors.log.2 # Error backup 2
```

**Rotation**: Files rotate when they reach 10MB (configurable)
**Retention**: Keeps 5 backup files (configurable)

## 🎨 Log Output Examples

### Console Output (Development)

```
[2025-11-13 14:30:15] INFO     - gemini_agent.__init__:44        - Initializing GeminiAgent with model=gemini-pro
[2025-11-13 14:30:15] DEBUG    - gemini_agent._is_gemini_installed:73 - Checking if Gemini CLI is installed
[2025-11-13 14:30:15] INFO     - gemini_agent.__init__:68        - GeminiAgent initialized successfully
[2025-11-13 14:30:16] INFO     - gemini_agent.query:105          - Starting Gemini query
[2025-11-13 14:30:18] INFO     - gemini_agent.query:125          - Gemini query completed in 2150.5ms
```

### JSON Output (Production)

```json
{
  "timestamp": "2025-11-13T14:30:15Z",
  "level": "INFO",
  "logger": "gemini_agent",
  "message": "Initializing GeminiAgent with model=gemini-pro",
  "module": "gemini_agent",
  "function": "__init__",
  "line": 44
}
{
  "timestamp": "2025-11-13T14:30:18Z",
  "level": "INFO",
  "logger": "gemini_agent",
  "message": "Gemini query completed",
  "module": "gemini_agent",
  "function": "query",
  "line": 125,
  "duration_ms": 2150.5,
  "operation": "gemini_query",
  "status": "success"
}
```

## 🔍 Monitoring & Analysis

### Grep for Errors

```bash
# Find all errors
grep "ERROR" logs/ai_project.log

# Find errors in last hour
grep "ERROR" logs/ai_project.log | grep "$(date +%Y-%m-%d\ %H)"

# Count errors by type
grep "ERROR" logs/ai_project.log | cut -d'-' -f5 | sort | uniq -c
```

### Parse JSON Logs

```bash
# Extract all error messages
cat logs/ai_project.log | jq 'select(.level=="ERROR") | .message'

# Calculate average duration
cat logs/ai_project.log | jq 'select(.duration_ms) | .duration_ms' | awk '{sum+=$1; count++} END {print sum/count}'

# Find slow operations (>1000ms)
cat logs/ai_project.log | jq 'select(.duration_ms > 1000)'
```

### Monitor in Real-Time

```bash
# Tail logs
tail -f logs/ai_project.log

# Tail with filtering
tail -f logs/ai_project.log | grep "ERROR\|WARNING"

# Tail JSON logs with formatting
tail -f logs/ai_project.log | jq '.'
```

## 📚 Integration Examples

### Gemini Agent

```python
from logging_config import get_logger

logger = get_logger(__name__)

class GeminiAgent:
    def __init__(self, api_key):
        logger.info("Initializing GeminiAgent")
        self.api_key = api_key
        logger.debug(f"API key configured (length: {len(api_key)})")
    
    def query(self, prompt):
        logger.info(f"Gemini query started (prompt length: {len(prompt)})")
        
        try:
            result = self._make_request(prompt)
            logger.info("Gemini query succeeded", extra={
                "response_length": len(result),
                "tokens": result.get("usage", {}).get("total_tokens")
            })
            return result
        except Exception as e:
            logger.error(f"Gemini query failed: {e}", exc_info=True)
            raise
```

### Claude Agent

```python
from logging_config import get_logger, log_performance

logger = get_logger(__name__)

class ClaudeAgent:
    @log_performance(logger, "claude_query")
    def query(self, prompt):
        logger.info("Claude query started")
        # Automatically logs duration and status
        return self._execute_query(prompt)
```

### Integration Tests

```python
from logging_config import get_logger

logger = get_logger(__name__)

@pytest.mark.integration
def test_api_call():
    logger.info("Starting API integration test")
    
    agent = GeminiAgent(api_key=os.getenv("GEMINI_API_KEY"))
    
    try:
        result = agent.query("test prompt")
        logger.info(f"Test passed: received {len(result)} bytes")
        assert result is not None
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        raise
```

## 🎯 Implementation Checklist

- [ ] Import logging_config in each module
- [ ] Initialize logger with `get_logger(__name__)`
- [ ] Log initialization in `__init__` methods
- [ ] Log function entry/exit for important operations
- [ ] Log all API calls (start, success, failure)
- [ ] Log errors with `exc_info=True` or `.exception()`
- [ ] Add performance logging for slow operations
- [ ] Include context in log messages (IDs, counts, etc.)
- [ ] Use appropriate log levels
- [ ] Never log sensitive data (API keys, passwords)
- [ ] Configure via environment variables
- [ ] Set up log rotation for production
- [ ] Add monitoring/alerting for ERROR+ logs

## 📖 Additional Resources

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Logging Best Practices](https://docs.python-guide.org/writing/logging/)
- [Structured Logging](https://www.structlog.org/en/stable/)
- [Log Analysis Tools](https://www.elastic.co/what-is/elk-stack)

---

**Next Steps**: See `LOGGING_IMPLEMENTATION.md` for step-by-step guide to add logging to existing code.
