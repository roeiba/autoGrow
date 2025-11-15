# Claude Agent Tests (Legacy)

**Note**: This directory previously contained tests for the legacy Docker-based agentic workflow.

The current tests for the Claude CLI agent are located in:
- **Unit tests**: `/tests/unit/test_claude_cli_agent.py`
- **Integration tests**: `/tests/integration/test_claude_cli_agent_integration.py`

## Why This Directory Exists

This directory is kept for potential future Docker-based workflow tests.

The original Docker-based Claude agent:
- Uses GitHub CLI for issue management
- Runs in a Docker container
- Uses the Anthropic API directly

## Current Testing

For the Claude CLI headless mode (current focus), use:

```bash
# Run unit tests
cd tests
pytest unit/test_claude_cli_agent.py -v

# Run integration tests
pytest integration/test_claude_cli_agent_integration.py -v -m integration
```

## Legacy Tests Removed

The legacy `test_agentic_workflow.py` has been removed because:
1. It tested the Docker-based workflow, not the CLI
2. It required different dependencies not in current setup
3. It's not part of the current CI/CD pipeline
4. It was causing CI failures

If Docker-based workflow tests are needed in the future:
1. Create new test files in this directory
2. Ensure dependencies are installed
3. Update CI/CD to run these tests separately
