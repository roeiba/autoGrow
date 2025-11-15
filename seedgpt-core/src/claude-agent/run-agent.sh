#!/bin/bash
set -e

# Claude Agent Runner Script
# Usage: ./run-agent.sh [repo_url] [issue_number]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found"
    echo "Please copy .env.example to .env and configure your credentials"
    exit 1
fi

# Load environment variables
source .env

# Override with command line arguments if provided
if [ -n "$1" ]; then
    export REPO_URL="$1"
    echo "Using repository: $REPO_URL"
fi

if [ -n "$2" ]; then
    export ISSUE_NUMBER="$2"
    echo "Using issue number: $ISSUE_NUMBER"
fi

# Validate required variables
if [ -z "$GITHUB_TOKEN" ]; then
    echo "ERROR: GITHUB_TOKEN not set in .env"
    exit 1
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ERROR: ANTHROPIC_API_KEY not set in .env"
    exit 1
fi

if [ -z "$REPO_URL" ]; then
    echo "ERROR: REPO_URL not set. Provide it in .env or as first argument"
    echo "Usage: ./run-agent.sh <repo_url> [issue_number]"
    exit 1
fi

echo "=== Claude Agent Runner ==="
echo "Repository: $REPO_URL"
echo "Issue: ${ISSUE_NUMBER:-auto-select}"
echo ""

# Build the image if it doesn't exist
if ! docker images | grep -q claude-agent; then
    echo "Building Docker image..."
    docker-compose build
fi

# Run the agent
echo "Starting agent..."
docker-compose up

echo ""
echo "=== Agent execution completed ==="
