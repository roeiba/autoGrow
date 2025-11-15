#!/bin/bash

# Automated Code Review using Claude CLI in headless mode
# Usage: ./code_review_cli.sh <file_or_directory>

set -e

# Check if claude CLI is installed
if ! command -v claude &> /dev/null; then
    echo "❌ Error: Claude Code CLI is not installed"
    echo "Install it from: https://code.claude.com/"
    exit 1
fi

TARGET="${1:-.}"
OUTPUT_DIR="./output/code-reviews-cli"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$OUTPUT_DIR"

echo "🔍 Starting Claude CLI code review for: $TARGET"
echo ""

if [ -f "$TARGET" ]; then
    # Single file review
    FILENAME=$(basename "$TARGET")
    OUTPUT_FILE="$OUTPUT_DIR/${FILENAME}_review_${TIMESTAMP}.json"
    
    echo "📄 Reviewing file: $FILENAME"
    
    result=$(cat "$TARGET" | claude -p "Review this code for:
    1. Security vulnerabilities
    2. Performance issues
    3. Code quality and best practices
    4. Potential bugs
    5. Suggestions for improvement
    
    Provide a structured analysis with severity levels." \
    --output-format json \
    --allowedTools "Read")
    
    echo "$result" > "$OUTPUT_FILE"
    echo "$result" | jq -r '.result' > "$OUTPUT_DIR/${FILENAME}_review_${TIMESTAMP}.txt" 2>/dev/null || \
        echo "$result" > "$OUTPUT_DIR/${FILENAME}_review_${TIMESTAMP}.txt"
    
    echo "✅ Review completed: $OUTPUT_FILE"
    echo ""
    echo "Summary:"
    cat "$OUTPUT_DIR/${FILENAME}_review_${TIMESTAMP}.txt" | head -20
    
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
        
        result=$(cat "$file" | claude -p "Quick code review: identify critical issues, security vulnerabilities, and major improvements needed." \
        --output-format json \
        --allowedTools "Read")
        
        echo "File: $file" >> "$SUMMARY_FILE"
        echo "$result" | jq -r '.result' >> "$SUMMARY_FILE" 2>/dev/null || echo "$result" >> "$SUMMARY_FILE"
        echo "" >> "$SUMMARY_FILE"
        echo "---" >> "$SUMMARY_FILE"
        echo "" >> "$SUMMARY_FILE"
        
        # Small delay to avoid rate limiting
        sleep 1
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
