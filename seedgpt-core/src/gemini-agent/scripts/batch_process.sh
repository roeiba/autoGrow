#!/bin/bash

# Batch process files using Gemini CLI in headless mode
# Usage: ./batch_process.sh <directory> <prompt>

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
    echo "Install it with: npm install -g @google/gemini-cli"
    exit 1
fi

DIRECTORY="${1}"
PROMPT="${2:-Analyze this file and provide insights}"
OUTPUT_DIR="./output/batch-processing"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PROGRESS_LOG="$OUTPUT_DIR/progress_${TIMESTAMP}.log"

mkdir -p "$OUTPUT_DIR"

if [ -z "$DIRECTORY" ]; then
    echo "❌ Error: Please provide a directory"
    echo "Usage: ./batch_process.sh <directory> [prompt]"
    echo ""
    echo "Example:"
    echo "  ./batch_process.sh ../src 'Find potential bugs'"
    exit 1
fi

if [ ! -d "$DIRECTORY" ]; then
    echo "❌ Error: Directory not found: $DIRECTORY"
    exit 1
fi

echo "🚀 Starting batch processing..."
echo "Directory: $DIRECTORY"
echo "Prompt: $PROMPT"
echo "Output: $OUTPUT_DIR"
echo ""

# Find all code files
FILES=$(find "$DIRECTORY" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" -o -name "*.go" -o -name "*.md" \))

if [ -z "$FILES" ]; then
    echo "⚠️  No files found in $DIRECTORY"
    exit 1
fi

FILE_COUNT=$(echo "$FILES" | wc -l | tr -d ' ')
echo "📊 Found $FILE_COUNT files to process"
echo ""

# Initialize progress log
echo "Batch Processing Log - $(date)" > "$PROGRESS_LOG"
echo "Directory: $DIRECTORY" >> "$PROGRESS_LOG"
echo "Prompt: $PROMPT" >> "$PROGRESS_LOG"
echo "Total files: $FILE_COUNT" >> "$PROGRESS_LOG"
echo "======================================" >> "$PROGRESS_LOG"
echo "" >> "$PROGRESS_LOG"

CURRENT=0
SUCCESSFUL=0
FAILED=0

for file in $FILES; do
    CURRENT=$((CURRENT + 1))
    FILENAME=$(basename "$file")
    RELATIVE_PATH=$(echo "$file" | sed "s|$DIRECTORY/||")
    
    echo "[$CURRENT/$FILE_COUNT] Processing: $RELATIVE_PATH"
    
    # Create output filename
    OUTPUT_FILE="$OUTPUT_DIR/${FILENAME}_result_${TIMESTAMP}.json"
    TEXT_OUTPUT="$OUTPUT_DIR/${FILENAME}_result_${TIMESTAMP}.txt"
    
    # Process file with Gemini
    if result=$(cat "$file" | gemini -p "$PROMPT" --output-format json -m gemini-2.5-flash 2>&1); then
        echo "$result" > "$OUTPUT_FILE"
        echo "$result" | jq -r '.response' > "$TEXT_OUTPUT" 2>/dev/null || echo "$result" > "$TEXT_OUTPUT"
        
        SUCCESSFUL=$((SUCCESSFUL + 1))
        echo "  ✅ Success: $OUTPUT_FILE"
        
        # Log to progress file
        echo "✅ $RELATIVE_PATH" >> "$PROGRESS_LOG"
        echo "   Output: $OUTPUT_FILE" >> "$PROGRESS_LOG"
        
        # Get token usage if available
        if echo "$result" | jq -e '.stats.models' > /dev/null 2>&1; then
            TOKENS=$(echo "$result" | jq -r '.stats.models // {} | to_entries | map(.value.tokens.total) | add // 0')
            echo "   Tokens: $TOKENS" >> "$PROGRESS_LOG"
        fi
        
        echo "" >> "$PROGRESS_LOG"
    else
        FAILED=$((FAILED + 1))
        echo "  ❌ Failed: $FILENAME"
        echo "  Error: $result"
        
        # Log failure
        echo "❌ $RELATIVE_PATH" >> "$PROGRESS_LOG"
        echo "   Error: $result" >> "$PROGRESS_LOG"
        echo "" >> "$PROGRESS_LOG"
    fi
    
    # Small delay to avoid rate limiting
    sleep 1
done

echo ""
echo "========================================"
echo "📊 Batch Processing Complete"
echo "========================================"
echo "Total files: $FILE_COUNT"
echo "Successful: $SUCCESSFUL"
echo "Failed: $FAILED"
echo ""
echo "📁 Results saved in: $OUTPUT_DIR"
echo "📋 Progress log: $PROGRESS_LOG"

# Generate summary report
SUMMARY_FILE="$OUTPUT_DIR/summary_${TIMESTAMP}.txt"
echo "Batch Processing Summary" > "$SUMMARY_FILE"
echo "Generated: $(date)" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "Directory: $DIRECTORY" >> "$SUMMARY_FILE"
echo "Prompt: $PROMPT" >> "$SUMMARY_FILE"
echo "Total files: $FILE_COUNT" >> "$SUMMARY_FILE"
echo "Successful: $SUCCESSFUL" >> "$SUMMARY_FILE"
echo "Failed: $FAILED" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "Results directory: $OUTPUT_DIR" >> "$SUMMARY_FILE"

echo ""
echo "📄 Summary: $SUMMARY_FILE"
