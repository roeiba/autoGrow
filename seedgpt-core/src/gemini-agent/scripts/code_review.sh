#!/bin/bash

# Automated Code Review using Gemini CLI in headless mode
# Usage: ./code_review.sh <file_or_directory>

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

TARGET="${1:-.}"
OUTPUT_DIR="./output/code-reviews"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$OUTPUT_DIR"

echo "🔍 Starting code review for: $TARGET"
echo ""

if [ -f "$TARGET" ]; then
    # Single file review
    FILENAME=$(basename "$TARGET")
    OUTPUT_FILE="$OUTPUT_DIR/${FILENAME}_review_${TIMESTAMP}.json"
    
    echo "📄 Reviewing file: $FILENAME"
    
    result=$(cat "$TARGET" | gemini -p "Review this code for:
    1. Security vulnerabilities
    2. Performance issues
    3. Code quality and best practices
    4. Potential bugs
    5. Suggestions for improvement
    
    Provide a structured analysis with severity levels." \
    --output-format json \
    -m gemini-2.5-pro)
    
    echo "$result" > "$OUTPUT_FILE"
    echo "$result" | jq -r '.response' > "$OUTPUT_DIR/${FILENAME}_review_${TIMESTAMP}.txt"
    
    echo "✅ Review completed: $OUTPUT_FILE"
    echo ""
    echo "Summary:"
    echo "$result" | jq -r '.response' | head -20
    
elif [ -d "$TARGET" ]; then
    # Directory review
    echo "📁 Reviewing directory: $TARGET"
    
    # Find all code files
    FILES=$(find "$TARGET" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" -o -name "*.go" \))
    
    if [ -z "$FILES" ]; then
        echo "⚠️  No code files found in $TARGET"
        exit 1
    fi
    
    SUMMARY_FILE="$OUTPUT_DIR/directory_review_${TIMESTAMP}.txt"
    echo "Code Review Summary - $(date)" > "$SUMMARY_FILE"
    echo "Target: $TARGET" >> "$SUMMARY_FILE"
    echo "======================================" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"
    
    for file in $FILES; do
        FILENAME=$(basename "$file")
        echo "  📄 Reviewing: $FILENAME"
        
        result=$(cat "$file" | gemini -p "Quick code review: identify critical issues, security vulnerabilities, and major improvements needed." \
        --output-format json \
        -m gemini-2.5-flash)
        
        echo "File: $file" >> "$SUMMARY_FILE"
        echo "$result" | jq -r '.response' >> "$SUMMARY_FILE"
        echo "" >> "$SUMMARY_FILE"
        echo "---" >> "$SUMMARY_FILE"
        echo "" >> "$SUMMARY_FILE"
    done
    
    echo "✅ Directory review completed: $SUMMARY_FILE"
    echo ""
    echo "Summary preview:"
    head -30 "$SUMMARY_FILE"
else
    echo "❌ Error: $TARGET is not a valid file or directory"
    exit 1
fi

echo ""
echo "📊 Review files saved in: $OUTPUT_DIR"
