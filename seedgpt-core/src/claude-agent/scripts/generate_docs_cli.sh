#!/bin/bash

# Generate documentation using Claude CLI in headless mode
# Usage: ./generate_docs_cli.sh <file_or_directory>

set -e

# Check if claude CLI is installed
if ! command -v claude &> /dev/null; then
    echo "❌ Error: Claude Code CLI is not installed"
    echo "Install it from: https://code.claude.com/"
    exit 1
fi

TARGET="${1:-.}"
OUTPUT_DIR="./output/docs-cli"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$OUTPUT_DIR"

echo "📚 Generating documentation with Claude CLI for: $TARGET"
echo ""

if [ -f "$TARGET" ]; then
    # Single file documentation
    FILENAME=$(basename "$TARGET")
    BASE_NAME="${FILENAME%.*}"
    OUTPUT_FILE="$OUTPUT_DIR/${BASE_NAME}_docs_${TIMESTAMP}.md"
    
    echo "📄 Documenting file: $FILENAME"
    
    result=$(cat "$TARGET" | claude -p "Generate comprehensive documentation for this code including:
    1. Overview and purpose
    2. Function/class descriptions
    3. Parameters and return values
    4. Usage examples
    5. Dependencies
    
    Format as Markdown." \
    --output-format json \
    --allowedTools "Read")
    
    echo "$result" | jq -r '.result' > "$OUTPUT_FILE" 2>/dev/null || echo "$result" > "$OUTPUT_FILE"
    
    echo "✅ Documentation generated: $OUTPUT_FILE"
    echo ""
    echo "Preview:"
    head -30 "$OUTPUT_FILE"
    
elif [ -d "$TARGET" ]; then
    # Directory documentation
    echo "📁 Documenting directory: $TARGET"
    
    # Generate README
    README_FILE="$OUTPUT_DIR/README_${TIMESTAMP}.md"
    
    # Get directory structure
    STRUCTURE=$(tree -L 3 "$TARGET" 2>/dev/null || find "$TARGET" -maxdepth 3 -type f -o -type d | head -50)
    
    result=$(echo "$STRUCTURE" | claude -p "Based on this project structure, generate a comprehensive README.md including:
    1. Project overview
    2. Directory structure explanation
    3. Setup instructions
    4. Usage guide
    5. Key features
    
    Format as Markdown." \
    --output-format json \
    --allowedTools "Read")
    
    echo "$result" | jq -r '.result' > "$README_FILE" 2>/dev/null || echo "$result" > "$README_FILE"
    
    echo "✅ README generated: $README_FILE"
    
    # Generate API documentation for code files
    API_DOC_FILE="$OUTPUT_DIR/API_DOCS_${TIMESTAMP}.md"
    echo "# API Documentation" > "$API_DOC_FILE"
    echo "Generated: $(date)" >> "$API_DOC_FILE"
    echo "" >> "$API_DOC_FILE"
    
    FILES=$(find "$TARGET" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" \) | head -10)
    
    for file in $FILES; do
        FILENAME=$(basename "$file")
        echo "  📄 Documenting: $FILENAME"
        
        echo "## $FILENAME" >> "$API_DOC_FILE"
        echo "" >> "$API_DOC_FILE"
        
        result=$(cat "$file" | claude -p "Generate API documentation for this code. Include function signatures, parameters, return values, and examples. Be concise." \
        --output-format json \
        --allowedTools "Read")
        
        echo "$result" | jq -r '.result' >> "$API_DOC_FILE" 2>/dev/null || echo "$result" >> "$API_DOC_FILE"
        echo "" >> "$API_DOC_FILE"
        echo "---" >> "$API_DOC_FILE"
        echo "" >> "$API_DOC_FILE"
        
        # Small delay
        sleep 1
    done
    
    echo "✅ API documentation generated: $API_DOC_FILE"
else
    echo "❌ Error: $TARGET is not a valid file or directory"
    exit 1
fi

echo ""
echo "📊 Documentation saved in: $OUTPUT_DIR"
