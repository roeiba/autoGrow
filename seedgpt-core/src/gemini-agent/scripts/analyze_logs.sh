#!/bin/bash

# Analyze log files using Gemini CLI in headless mode
# Usage: ./analyze_logs.sh <log_file>

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

LOG_FILE="${1}"
OUTPUT_DIR="./output/log-analysis"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$OUTPUT_DIR"

if [ -z "$LOG_FILE" ]; then
    echo "❌ Error: Please provide a log file"
    echo "Usage: ./analyze_logs.sh <log_file>"
    exit 1
fi

if [ ! -f "$LOG_FILE" ]; then
    echo "❌ Error: Log file not found: $LOG_FILE"
    exit 1
fi

echo "🔍 Analyzing log file: $LOG_FILE"
echo ""

# Extract errors
echo "📊 Extracting errors..."
ERRORS=$(grep -i "error\|exception\|fatal\|critical" "$LOG_FILE" | tail -100 || echo "No errors found")

# Extract warnings
echo "⚠️  Extracting warnings..."
WARNINGS=$(grep -i "warn\|warning" "$LOG_FILE" | tail -50 || echo "No warnings found")

# Get log statistics
TOTAL_LINES=$(wc -l < "$LOG_FILE")
ERROR_COUNT=$(grep -ic "error\|exception\|fatal\|critical" "$LOG_FILE" || echo "0")
WARNING_COUNT=$(grep -ic "warn\|warning" "$LOG_FILE" || echo "0")

echo "📈 Log Statistics:"
echo "  Total lines: $TOTAL_LINES"
echo "  Errors: $ERROR_COUNT"
echo "  Warnings: $WARNING_COUNT"
echo ""

# Analyze errors
if [ "$ERROR_COUNT" -gt 0 ]; then
    echo "🤖 Analyzing errors with Gemini..."
    
    OUTPUT_FILE="$OUTPUT_DIR/error_analysis_${TIMESTAMP}.json"
    
    result=$(echo "$ERRORS" | gemini -p "Analyze these log errors and provide:
    1. Root cause analysis
    2. Severity assessment
    3. Recommended fixes
    4. Prevention strategies
    5. Related patterns or issues
    
    Group similar errors together." \
    --output-format json \
    -m gemini-2.5-pro)
    
    echo "$result" > "$OUTPUT_FILE"
    echo "$result" | jq -r '.response' > "$OUTPUT_DIR/error_analysis_${TIMESTAMP}.txt"
    
    echo "✅ Error analysis completed: $OUTPUT_FILE"
    echo ""
    echo "Summary:"
    echo "$result" | jq -r '.response' | head -40
fi

# Analyze warnings if present
if [ "$WARNING_COUNT" -gt 0 ]; then
    echo ""
    echo "🤖 Analyzing warnings with Gemini..."
    
    WARNING_OUTPUT="$OUTPUT_DIR/warning_analysis_${TIMESTAMP}.txt"
    
    result=$(echo "$WARNINGS" | gemini -p "Analyze these log warnings and provide:
    1. Potential issues
    2. Priority level
    3. Recommended actions
    
    Be concise." \
    --output-format json \
    -m gemini-2.5-flash)
    
    echo "$result" | jq -r '.response' > "$WARNING_OUTPUT"
    
    echo "✅ Warning analysis completed: $WARNING_OUTPUT"
fi

# Generate overall summary
echo ""
echo "🤖 Generating overall log summary..."

SUMMARY_OUTPUT="$OUTPUT_DIR/log_summary_${TIMESTAMP}.txt"

# Get a sample of the log
LOG_SAMPLE=$(tail -200 "$LOG_FILE")

result=$(echo "$LOG_SAMPLE" | gemini -p "Analyze this log sample and provide:
1. Overall system health assessment
2. Key patterns or trends
3. Critical issues requiring immediate attention
4. Recommendations for monitoring and alerting

Statistics:
- Total lines: $TOTAL_LINES
- Errors: $ERROR_COUNT
- Warnings: $WARNING_COUNT" \
--output-format json \
-m gemini-2.5-pro)

echo "$result" | jq -r '.response' > "$SUMMARY_OUTPUT"

echo "✅ Log summary completed: $SUMMARY_OUTPUT"
echo ""
echo "Summary preview:"
cat "$SUMMARY_OUTPUT"

echo ""
echo "📊 All analysis files saved in: $OUTPUT_DIR"
