#!/bin/bash
set -e

echo "=== Claude Agentic Workflow Executor Starting ==="
echo "Repository: ${REPO_URL}"
echo "Issue Number: ${ISSUE_NUMBER:-'auto-select'}"
echo "Mode: ${AGENT_MODE}"

# Validate required environment variables
if [ -z "$GITHUB_TOKEN" ]; then
    echo "ERROR: GITHUB_TOKEN is required"
    exit 1
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ERROR: ANTHROPIC_API_KEY is required"
    exit 1
fi

if [ -z "$REPO_URL" ]; then
    echo "ERROR: REPO_URL is required"
    exit 1
fi

# Authenticate with GitHub CLI (for any shell commands that might need it)
echo "$GITHUB_TOKEN" | gh auth login --with-token

# Verify authentication
gh auth status

# Execute the Python agentic workflow
echo "Executing Python agentic workflow..."
python3 /agent/src/agentic_workflow.py

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "=== Claude Agentic Workflow Executor Completed Successfully ==="
else
    echo "=== Claude Agentic Workflow Executor Failed with exit code $exit_code ==="
fi

exit $exit_code
