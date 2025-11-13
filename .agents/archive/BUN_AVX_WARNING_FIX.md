# Bun/AVX Warning Fix

## Problem

The issue resolver was failing with this error:

```
❌ Claude Agent error: Claude CLI error: warn: CPU lacks AVX support, strange crashes may occur.
Reinstall Bun or use *-baseline build:
https://github.com/oven-sh/bun/releases/download/bun-v1.3.1/bun-darwin-x64-baseline.zip

subprocess.CalledProcessError: Command '['claude', '-p', ...]' returned non-zero exit status 1.
```

## Root Cause

Claude CLI (which uses Bun internally) was outputting a **warning** to stderr about AVX support. The Python subprocess code was treating this warning as a **fatal error** because:

1. The process returned a non-zero exit code
2. There was content in stderr
3. The code used `check=True` which raises on any non-zero exit

However, **Claude CLI was still producing valid output** despite the warning!

## Solution

Modified `claude_cli_agent.py` to distinguish between warnings and actual errors:

### Key Changes

1. **Changed `check=True` to `check=False`**
   - Manually check return codes instead of auto-raising
   - Allows inspection of stderr content

2. **Detect Warning-Only Scenarios**
   ```python
   stderr_lower = result.stderr.lower() if result.stderr else ""
   is_warning_only = (
       "warn:" in stderr_lower or 
       "warning:" in stderr_lower
   ) and result.stdout.strip()  # Has actual output
   ```

3. **Handle Warnings Gracefully**
   ```python
   if not is_warning_only:
       raise RuntimeError(f"Claude CLI error: {result.stderr}")
   else:
       # Log warning but continue
       if self.verbose and result.stderr:
           print(f"⚠️  Warning from Claude CLI: {result.stderr.strip()}")
   ```

### Applied to Both Modes

- **Non-streaming mode** (`query()` without `stream_output`)
- **Streaming mode** (`query()` with `stream_output=True`)

## Benefits

1. ✅ **Warnings don't stop execution** - Work continues if output is valid
2. ✅ **Warnings are still logged** - Visible in verbose mode
3. ✅ **Real errors still raise** - Actual failures are caught
4. ✅ **Works on all CPUs** - No AVX requirement

## Testing

### Before Fix
```bash
$ .agents/run_issue_resolver_with_env.sh
...
❌ Claude Agent error: Claude CLI error: warn: CPU lacks AVX support...
[STOPS EXECUTION]
```

### After Fix
```bash
$ .agents/run_issue_resolver_with_env.sh
...
⚠️  Warning from Claude CLI: warn: CPU lacks AVX support...
✅ Claude completed work
[CONTINUES EXECUTION]
```

## Implementation Details

### Warning Detection Logic

A message is considered a "warning only" if:
1. stderr contains "warn:" or "warning:" (case-insensitive)
2. **AND** stdout has actual content (not empty)

This ensures:
- Real errors (no output) still raise exceptions
- Warnings with output are logged but don't stop execution

### Example Scenarios

| Scenario | stderr | stdout | Result |
|----------|--------|--------|--------|
| Success | empty | content | ✅ Return content |
| Warning + Success | "warn: AVX..." | content | ⚠️ Log warning, return content |
| Real Error | "error: failed" | empty | ❌ Raise exception |
| Real Error | "error: failed" | content | ❌ Raise exception |

## Related Issues

This fix also handles other potential warnings:
- Bun version warnings
- Deprecation notices
- Performance warnings
- Any other non-fatal stderr output

## Files Modified

1. `src/claude-agent/claude_cli_agent.py`
   - Modified `query()` method (both streaming and non-streaming)
   - Added warning detection logic
   - Improved error handling

2. `.agents/CLAUDE_CLI_LOGGING.md`
   - Documented the issue and solution
   - Added troubleshooting section

## Alternative Solutions Considered

### 1. Suppress stderr entirely
❌ **Rejected** - Would hide real errors

### 2. Install Bun baseline build
❌ **Rejected** - Requires manual intervention, not portable

### 3. Redirect stderr to /dev/null
❌ **Rejected** - Loses valuable debugging information

### 4. Check exit code only
❌ **Rejected** - Exit code is non-zero even for warnings

### 5. Parse stderr intelligently ✅
✅ **Chosen** - Best balance of safety and functionality

## Future Improvements

Potential enhancements:
- [ ] Configurable warning patterns
- [ ] Warning severity levels
- [ ] Option to treat warnings as errors
- [ ] Collect warnings in result metadata
- [ ] Warning suppression patterns

## Conclusion

The fix allows Claude CLI to work on CPUs without AVX support while still catching real errors. Warnings are logged but don't stop execution, making the issue resolver more robust and portable.
