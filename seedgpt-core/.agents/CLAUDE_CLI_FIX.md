# Claude CLI Authentication Fix for GitHub Actions

## Problem
The GitHub Actions workflow for `issue-resolver.yml` was failing because:
1. Claude CLI requires authentication to work
2. In CI/CD environments, interactive authentication is not possible
3. The code was trying to use Claude CLI without proper API key configuration

## Solution
Claude CLI supports **headless authentication** via environment variables:

### Key Environment Variables
- `ANTHROPIC_API_KEY` - Claude CLI automatically uses this for API authentication
- `GITHUB_TOKEN` - Used for GitHub operations (already configured)
- `DISABLE_TELEMETRY` - Disables telemetry in CI/CD
- `DISABLE_ERROR_REPORTING` - Disables error reporting in CI/CD
- `DISABLE_AUTOUPDATER` - Prevents auto-update checks in CI/CD

## Changes Made

### 1. Updated `claude_cli_agent.py`
Added `require_cli` parameter to allow graceful handling when CLI is not available:
```python
def __init__(self, ..., require_cli: bool = True):
    self.cli_available = self._is_claude_installed()
    if require_cli and not self.cli_available:
        raise RuntimeError("Claude Code CLI is not installed...")
```

### 2. Updated `issue_resolver.py`
Implemented proper fallback mechanism:
- First tries Claude CLI if available (with API key authentication)
- Falls back to Anthropic SDK if CLI is not available
- Provides clear logging about which method is being used

### 3. Updated `.github/workflows/issue-resolver.yml`
Added Claude CLI environment variables:
```yaml
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  GITHUB_TOKEN: ${{ secrets.PAT_TOKEN }}
  DISABLE_TELEMETRY: "1"
  DISABLE_ERROR_REPORTING: "1"
  DISABLE_AUTOUPDATER: "1"
```

## How It Works

### With Claude CLI Headless Mode (Preferred)
1. Claude CLI is installed via npm: `npm install -g @anthropic-ai/claude-code`
2. `ANTHROPIC_API_KEY` environment variable provides authentication
3. Uses headless mode with `-p` flag for non-interactive execution
4. Command format: `claude -p "prompt" --allowedTools "Read,Write,Bash" --permission-mode acceptEdits`
5. Claude CLI has full file system access via Read/Write/Bash tools
6. Can make actual code changes directly

### Fallback to Anthropic SDK
1. If Claude CLI is not available or fails
2. Uses direct Anthropic API calls
3. Provides solution guidance (no direct file modifications)
4. Requires manual implementation of suggested changes

## Testing

### Local Testing
```bash
# Set environment variables
export ANTHROPIC_API_KEY="your-key"
export GITHUB_TOKEN="your-token"

# Run the agent
python .github/scripts/issue_resolver.py
```

### CI/CD Testing
The workflow will automatically:
1. Install Claude CLI via npm
2. Use ANTHROPIC_API_KEY for authentication
3. Execute the issue resolver with full capabilities

## Benefits
- ✅ Works in both local and CI/CD environments
- ✅ No interactive authentication required via headless mode
- ✅ Claude CLI can make actual code changes with file system access
- ✅ Graceful fallback if CLI is unavailable
- ✅ Clear logging and error messages
- ✅ Uses `--permission-mode acceptEdits` for automated workflows

## Headless Mode Details

### What is Headless Mode?
Headless mode allows Claude CLI to run programmatically without interactive UI:
- Uses `-p` or `--print` flag for non-interactive execution
- Accepts prompts via command line
- Outputs results to stdout
- Perfect for CI/CD automation

### Key Flags Used
```bash
claude -p "prompt"                    # Headless mode
  --allowedTools "Read,Write,Bash"    # Enable file system tools
  --permission-mode acceptEdits       # Auto-accept file edits
  --output-format text                # Text output (vs json)
  --verbose                           # Detailed logging
```

### Authentication in Headless Mode
- `ANTHROPIC_API_KEY` environment variable is automatically detected
- No interactive login required
- Works seamlessly in CI/CD pipelines

## References
- [Claude CLI Headless Mode](https://code.claude.com/docs/en/headless) - **Primary reference**
- [Claude CLI Setup](https://code.claude.com/docs/en/setup)
- [Claude CLI IAM](https://code.claude.com/docs/en/iam)
- [Claude CLI Settings](https://code.claude.com/docs/en/settings)
- [Claude GitHub Actions](https://code.claude.com/docs/en/github-actions)
