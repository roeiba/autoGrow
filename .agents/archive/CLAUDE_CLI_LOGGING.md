# Claude CLI Logging Guide

## Overview

This guide explains how to get detailed logs and real-time output when using Claude CLI in headless mode.

## Logging Options

### 1. Verbose Mode (`--verbose`)

The most important flag for debugging:

```bash
claude -p "your prompt" --verbose
```

**Benefits:**
- Shows detailed execution steps
- Displays tool calls and results
- Provides timing information
- Shows API interactions

### 2. Streaming JSON Output (`--output-format stream-json`)

For real-time event streaming:

```bash
claude -p "your prompt" --output-format stream-json
```

**Benefits:**
- See events as they happen
- Monitor progress in real-time
- Useful for long-running tasks
- Can parse events programmatically

**Event Types:**
- `init` - Initialization
- `tool_use` - Tool execution
- `result` - Final result

### 3. JSON Output (`--output-format json`)

For structured results with metadata:

```bash
claude -p "your prompt" --output-format json
```

**Returns:**
```json
{
  "type": "result",
  "subtype": "success",
  "total_cost_usd": 0.003,
  "is_error": false,
  "duration_ms": 1234,
  "duration_api_ms": 800,
  "num_turns": 6,
  "result": "The response text here...",
  "session_id": "abc123"
}
```

**Metadata Includes:**
- `duration_ms` - Total execution time
- `duration_api_ms` - API call duration
- `num_turns` - Number of conversation turns
- `total_cost_usd` - Cost of the operation
- `session_id` - Session identifier for resuming

## Implementation in `claude_cli_agent.py`

### Updated `query()` Method

Added `stream_output` parameter for real-time logging:

```python
def query(
    self,
    prompt: str,
    system_prompt: Optional[str] = None,
    mcp_config: Optional[str] = None,
    stream_output: bool = False  # NEW
) -> Dict[str, Any]:
    """Send a query with optional streaming output"""
```

### Streaming Implementation

```python
if stream_output:
    # Stream output in real-time
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1  # Line buffered
    )
    
    # Print output as it arrives
    for line in process.stdout:
        print(line, end='', flush=True)
        stdout_lines.append(line)
```

## Usage in Issue Resolver

### Before (No Logs)
```python
agent = ClaudeAgent(output_format="text")
result = agent.query(prompt)
# No visibility into what's happening
```

### After (With Logs)
```python
agent = ClaudeAgent(
    output_format="text",
    verbose=True,  # Enable verbose logging
    allowed_tools=["Read", "Write", "Bash"],
    permission_mode="acceptEdits"
)

print("📤 Sending query to Claude (streaming output)...")
print("-" * 60)
result = agent.query(prompt, stream_output=True)  # Stream output
print("-" * 60)
```

## Example Output

### With Verbose + Streaming

```
📤 Sending query to Claude (streaming output)...
------------------------------------------------------------
🔍 Reading file: src/utils/validator.py
📝 Analyzing structure...
✍️  Writing file: src/utils/new_validator.py
🧪 Running tests...
✅ Tests passed
📊 Summary: Created validator with 350 lines
------------------------------------------------------------
✅ Claude completed work
📊 Summary length: 1234 chars
```

## Best Practices

### 1. Always Use Verbose in Development
```python
agent = ClaudeAgent(verbose=True)  # Always for debugging
```

### 2. Stream Output for Long Tasks
```python
result = agent.query(prompt, stream_output=True)  # See progress
```

### 3. Use JSON Format for Metadata
```python
agent = ClaudeAgent(output_format="json")
result = agent.query(prompt)
print(f"Cost: ${result['total_cost_usd']}")
print(f"Duration: {result['duration_ms']}ms")
print(f"Turns: {result['num_turns']}")
```

### 4. Capture Both stdout and stderr
```python
# Already implemented in updated query() method
if stderr_output:
    print(f"\nStderr: {stderr_output}", flush=True)
```

## Debugging Tips

### 1. Check Claude CLI Version
```bash
claude --version
```

### 2. Test with Simple Query
```bash
claude -p "Hello" --verbose
```

### 3. Check for Errors
```bash
claude -p "your query" --verbose 2>&1 | tee claude.log
```

### 4. Monitor File Changes
```bash
watch -n 1 'git status --short'
```

## Common Issues

### Issue: No Output During Execution
**Solution:** Use `stream_output=True` and `verbose=True`

### Issue: Can't See Tool Calls
**Solution:** Enable `--verbose` flag

### Issue: Unknown Duration/Cost
**Solution:** Use `--output-format json`

### Issue: Lost Output on Error
**Solution:** Capture stderr separately (already implemented)

### Issue: Bun/AVX Warning Treated as Fatal Error
**Problem:**
```
Claude CLI error: warn: CPU lacks AVX support, strange crashes may occur.
Reinstall Bun or use *-baseline build
```

**Solution:** 
The agent now distinguishes between warnings and actual errors. Warnings in stderr (containing "warn:" or "warning:") that still produce output are logged but don't stop execution.

**Implementation:**
```python
# Check if stderr contains only warnings (not actual errors)
stderr_lower = result.stderr.lower() if result.stderr else ""
is_warning_only = (
    "warn:" in stderr_lower or 
    "warning:" in stderr_lower
) and result.stdout.strip()  # Has actual output

if not is_warning_only:
    raise RuntimeError(f"Claude CLI error: {result.stderr}")
else:
    # Log warning but continue
    print(f"⚠️  Warning from Claude CLI: {result.stderr.strip()}")
```

## Configuration Examples

### Maximum Logging
```python
agent = ClaudeAgent(
    output_format="json",      # Get metadata
    verbose=True,              # Detailed logs
    allowed_tools=["Read", "Write", "Bash"],
    permission_mode="acceptEdits"
)

result = agent.query(
    prompt,
    stream_output=True  # Real-time output
)

print(f"Duration: {result['duration_ms']}ms")
print(f"Cost: ${result['total_cost_usd']}")
print(f"Turns: {result['num_turns']}")
```

### Production (Minimal Logging)
```python
agent = ClaudeAgent(
    output_format="json",
    verbose=False,  # Quiet mode
    permission_mode="acceptEdits"
)

result = agent.query(prompt, stream_output=False)
```

## Related Documentation

- [Claude CLI Headless Mode](https://code.claude.com/docs/en/headless)
- [CLI Reference](https://code.claude.com/docs/en/cli-reference)

## Summary

**Key Improvements:**
1. ✅ Added `--verbose` flag support
2. ✅ Implemented `stream_output` parameter
3. ✅ Real-time output streaming
4. ✅ Separate stdout/stderr capture
5. ✅ Better error messages

**Result:**
- Full visibility into Claude's execution
- Real-time progress monitoring
- Detailed metadata and timing
- Better debugging capabilities
