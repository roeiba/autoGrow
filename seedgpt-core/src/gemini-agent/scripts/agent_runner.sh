#!/bin/bash

# Gemini Agent Runner - Main script for running agent tasks
# Usage: ./agent_runner.sh <task> [options]

set -e

# Load environment variables if .env exists
if [ -f "../.env" ]; then
    export $(cat ../.env | grep -v '^#' | xargs)
fi

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY is not set"
    echo "Please set it in .env file or export it: export GEMINI_API_KEY='your-key'"
    exit 1
fi

# Check if gemini-cli is installed
if ! command -v gemini &> /dev/null; then
    echo "❌ Error: gemini-cli is not installed"
    echo ""
    echo "Install with one of these methods:"
    echo "  npm install -g @google/gemini-cli"
    echo "  brew install gemini-cli"
    exit 1
fi

TASK="${1}"

show_help() {
    echo "🤖 Gemini Agent Runner"
    echo ""
    echo "Usage: ./agent_runner.sh <task> [options]"
    echo ""
    echo "Available tasks:"
    echo "  code-review <file|dir>     - Review code for issues and improvements"
    echo "  generate-docs <file|dir>   - Generate documentation"
    echo "  analyze-logs <log_file>    - Analyze log files for errors and patterns"
    echo "  batch-process <dir> <prompt> - Process multiple files with custom prompt"
    echo "  custom <prompt>            - Run custom prompt in agent mode"
    echo ""
    echo "Examples:"
    echo "  ./agent_runner.sh code-review ../src/main.py"
    echo "  ./agent_runner.sh generate-docs ../src"
    echo "  ./agent_runner.sh analyze-logs /var/log/app.log"
    echo "  ./agent_runner.sh batch-process ../src 'Find security issues'"
    echo "  ./agent_runner.sh custom 'Explain the project structure'"
    echo ""
    echo "Options:"
    echo "  --model, -m <model>        - Specify Gemini model (default: gemini-2.5-pro)"
    echo "  --yolo, -y                 - Auto-approve all actions"
    echo "  --debug, -d                - Enable debug mode"
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
        ./code_review.sh "$TARGET"
        ;;
    
    generate-docs)
        TARGET="${2:-.}"
        echo "📚 Generating documentation for: $TARGET"
        ./generate_docs.sh "$TARGET"
        ;;
    
    analyze-logs)
        LOG_FILE="${2}"
        if [ -z "$LOG_FILE" ]; then
            echo "❌ Error: Please provide a log file"
            echo "Usage: ./agent_runner.sh analyze-logs <log_file>"
            exit 1
        fi
        echo "🔍 Analyzing logs: $LOG_FILE"
        ./analyze_logs.sh "$LOG_FILE"
        ;;
    
    batch-process)
        DIRECTORY="${2}"
        PROMPT="${3:-Analyze this file}"
        if [ -z "$DIRECTORY" ]; then
            echo "❌ Error: Please provide a directory"
            echo "Usage: ./agent_runner.sh batch-process <directory> [prompt]"
            exit 1
        fi
        echo "🚀 Batch processing: $DIRECTORY"
        ./batch_process.sh "$DIRECTORY" "$PROMPT"
        ;;
    
    custom)
        PROMPT="${2}"
        if [ -z "$PROMPT" ]; then
            echo "❌ Error: Please provide a prompt"
            echo "Usage: ./agent_runner.sh custom '<prompt>'"
            exit 1
        fi
        echo "🤖 Running custom prompt..."
        echo ""
        
        # Run with agent mode features
        gemini -p "$PROMPT" \
            --output-format json \
            -m gemini-2.5-pro \
            --include-directories ../.. \
            | jq -r '.response'
        ;;
    
    *)
        echo "❌ Error: Unknown task: $TASK"
        echo ""
        show_help
        exit 1
        ;;
esac
