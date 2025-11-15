#!/bin/bash

# Claude CLI Agent Runner - Main script for running agent tasks
# Usage: ./agent_runner_cli.sh <task> [options]

set -e

# Check if claude CLI is installed
if ! command -v claude &> /dev/null; then
    echo "❌ Error: Claude Code CLI is not installed"
    echo "Install it from: https://code.claude.com/"
    exit 1
fi

TASK="${1}"

show_help() {
    echo "🤖 Claude CLI Agent Runner"
    echo ""
    echo "Usage: ./agent_runner_cli.sh <task> [options]"
    echo ""
    echo "Available tasks:"
    echo "  code-review <file|dir>           - Review code for issues and improvements"
    echo "  generate-docs <file|dir>         - Generate documentation"
    echo "  fix-code <file> <issue>          - Fix specific code issues"
    echo "  custom <prompt>                  - Run custom prompt in agent mode"
    echo "  continue <prompt>                - Continue most recent conversation"
    echo "  resume <session_id> <prompt>     - Resume specific conversation"
    echo ""
    echo "Examples:"
    echo "  ./agent_runner_cli.sh code-review ../src/main.py"
    echo "  ./agent_runner_cli.sh generate-docs ../src"
    echo "  ./agent_runner_cli.sh fix-code app.py 'Fix memory leak'"
    echo "  ./agent_runner_cli.sh custom 'Explain the project structure'"
    echo "  ./agent_runner_cli.sh continue 'Now add tests'"
    echo "  ./agent_runner_cli.sh resume abc123 'Update documentation'"
    echo ""
    echo "Options:"
    echo "  --verbose, -v                    - Enable verbose mode"
    echo "  --output-format <format>         - Output format (text, json, stream-json)"
    echo "  --allowed-tools <tools>          - Comma-separated list of allowed tools"
    echo ""
}

if [ -z "$TASK" ] || [ "$TASK" = "help" ] || [ "$TASK" = "--help" ] || [ "$TASK" = "-h" ]; then
    show_help
    exit 0
fi

case "$TASK" in
    code-review)
        TARGET="${2:-.}"
        echo "🔍 Running code review on: $TARGET"
        ./code_review_cli.sh "$TARGET"
        ;;
    
    generate-docs)
        TARGET="${2:-.}"
        echo "📚 Generating documentation for: $TARGET"
        ./generate_docs_cli.sh "$TARGET"
        ;;
    
    fix-code)
        FILE="${2}"
        ISSUE="${3}"
        if [ -z "$FILE" ] || [ -z "$ISSUE" ]; then
            echo "❌ Error: Missing arguments"
            echo "Usage: ./agent_runner_cli.sh fix-code <file> <issue>"
            exit 1
        fi
        echo "🔧 Fixing code: $FILE"
        ./fix_code_cli.sh "$FILE" "$ISSUE"
        ;;
    
    custom)
        PROMPT="${2}"
        if [ -z "$PROMPT" ]; then
            echo "❌ Error: Please provide a prompt"
            echo "Usage: ./agent_runner_cli.sh custom '<prompt>'"
            exit 1
        fi
        echo "🤖 Running custom prompt..."
        echo ""
        
        claude -p "$PROMPT" \
            --output-format json \
            --allowedTools "Read,Write,Bash" \
            | jq -r '.result' 2>/dev/null || claude -p "$PROMPT"
        ;;
    
    continue)
        PROMPT="${2}"
        if [ -z "$PROMPT" ]; then
            echo "❌ Error: Please provide a prompt"
            echo "Usage: ./agent_runner_cli.sh continue '<prompt>'"
            exit 1
        fi
        echo "🔄 Continuing conversation..."
        echo ""
        
        claude --continue "$PROMPT" \
            --output-format json \
            | jq -r '.result' 2>/dev/null || claude --continue "$PROMPT"
        ;;
    
    resume)
        SESSION_ID="${2}"
        PROMPT="${3}"
        if [ -z "$SESSION_ID" ] || [ -z "$PROMPT" ]; then
            echo "❌ Error: Missing arguments"
            echo "Usage: ./agent_runner_cli.sh resume <session_id> '<prompt>'"
            exit 1
        fi
        echo "🔄 Resuming session: $SESSION_ID"
        echo ""
        
        claude --resume "$SESSION_ID" "$PROMPT" \
            --output-format json \
            | jq -r '.result' 2>/dev/null || claude --resume "$SESSION_ID" "$PROMPT"
        ;;
    
    *)
        echo "❌ Error: Unknown task: $TASK"
        echo ""
        show_help
        exit 1
        ;;
esac
