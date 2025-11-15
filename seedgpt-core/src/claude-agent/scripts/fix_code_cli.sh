#!/bin/bash

# Fix code issues using Claude CLI in headless mode
# Usage: ./fix_code_cli.sh <file> <issue_description>

set -e

# Check if claude CLI is installed
if ! command -v claude &> /dev/null; then
    echo "❌ Error: Claude Code CLI is not installed"
    echo "Install it from: https://code.claude.com/"
    exit 1
fi

FILE_PATH="${1}"
ISSUE_DESC="${2}"
OUTPUT_DIR="./output/fixes-cli"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$OUTPUT_DIR"

if [ -z "$FILE_PATH" ] || [ -z "$ISSUE_DESC" ]; then
    echo "❌ Error: Missing arguments"
    echo "Usage: ./fix_code_cli.sh <file> <issue_description>"
    echo ""
    echo "Example:"
    echo "  ./fix_code_cli.sh src/app.py 'Fix the memory leak in the data processing function'"
    exit 1
fi

if [ ! -f "$FILE_PATH" ]; then
    echo "❌ Error: File not found: $FILE_PATH"
    exit 1
fi

FILENAME=$(basename "$FILE_PATH")
OUTPUT_FILE="$OUTPUT_DIR/${FILENAME}_fix_${TIMESTAMP}.json"

echo "🔧 Fixing code with Claude CLI"
echo "File: $FILE_PATH"
echo "Issue: $ISSUE_DESC"
echo ""

result=$(cat "$FILE_PATH" | claude -p "Fix the following issue in this code:

Issue: $ISSUE_DESC

File: $FILE_PATH

Provide:
1. The fixed code
2. Explanation of changes
3. Testing recommendations

Format the response clearly." \
--output-format json \
--allowedTools "Read,Write" \
--permission-mode acceptEdits)

echo "$result" > "$OUTPUT_FILE"

# Extract and save the result
RESULT_TEXT=$(echo "$result" | jq -r '.result' 2>/dev/null || echo "$result")
echo "$RESULT_TEXT" > "$OUTPUT_DIR/${FILENAME}_fix_${TIMESTAMP}.txt"

echo "✅ Fix completed: $OUTPUT_FILE"
echo ""
echo "Fix Details:"
echo "$RESULT_TEXT"

# Check if there's a session ID for continuing
SESSION_ID=$(echo "$result" | jq -r '.session_id' 2>/dev/null || echo "")
if [ -n "$SESSION_ID" ] && [ "$SESSION_ID" != "null" ]; then
    echo ""
    echo "💡 Session ID: $SESSION_ID"
    echo "   Continue with: claude --resume $SESSION_ID 'additional prompt'"
fi

echo ""
echo "📊 Fix saved in: $OUTPUT_DIR"
