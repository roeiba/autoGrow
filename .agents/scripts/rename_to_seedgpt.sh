#!/bin/bash

# Rename AutoGrow to SeedGPT across the entire repository
# This script handles all case variations

set -e

PROJECT_ROOT="/Users/roei/dev_workspace/spring-clients-projects/ai-project-template"

echo "🌱 Starting rename from AutoGrow to SeedGPT..."

# Find all text files (excluding .git, node_modules, etc.)
find "$PROJECT_ROOT" -type f \
  -not -path "*/\.*" \
  -not -path "*/node_modules/*" \
  -not -path "*/venv/*" \
  -not -path "*/__pycache__/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -name "*.pyc" \
  -not -name "*.pyo" \
  -not -name "*.so" \
  -not -name "*.dylib" \
  -not -name "rename_to_seedgpt.sh" \
  | while read -r file; do
    
    # Check if file is a text file
    if file "$file" | grep -q "text\|empty\|JSON\|Python\|shell\|HTML\|XML\|YAML"; then
        # Create backup
        cp "$file" "$file.bak"
        
        # Perform replacements (order matters - do longer strings first)
        sed -i '' \
            -e 's/AutoGrow/SeedGPT/g' \
            -e 's/autogrow/seedgpt/g' \
            -e 's/AUTOGROW/SEEDGPT/g' \
            -e 's/autoGrow/seedGPT/g' \
            "$file"
        
        # Check if file changed
        if ! cmp -s "$file" "$file.bak"; then
            echo "✓ Updated: $file"
            rm "$file.bak"
        else
            # No changes, restore original
            mv "$file.bak" "$file"
        fi
    fi
done

echo ""
echo "✅ Rename complete!"
echo ""
echo "📝 Summary of changes:"
echo "   AutoGrow → SeedGPT"
echo "   autogrow → seedgpt"
echo "   AUTOGROW → SEEDGPT"
echo "   autoGrow → seedGPT"
echo ""
echo "🔍 Next steps:"
echo "   1. Review changes: git diff"
echo "   2. Test the application"
echo "   3. Commit: git add -A && git commit -m 'Rename AutoGrow to SeedGPT'"
