#!/bin/bash
# Verify Claude CLI setup and authentication

echo "🔍 Claude CLI Setup Verification"
echo "=================================="
echo ""

# Check if Claude CLI is installed
echo "1. Checking Claude CLI installation..."
if command -v claude &> /dev/null; then
    echo "   ✅ Claude CLI is installed"
    claude --version 2>&1 | head -n 1 || echo "   ⚠️  Version check failed (may be normal)"
else
    echo "   ❌ Claude CLI is NOT installed"
    echo "   Install with: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

echo ""
echo "2. Checking environment variables..."

# Check ANTHROPIC_API_KEY
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "   ✅ ANTHROPIC_API_KEY is set (${#ANTHROPIC_API_KEY} chars)"
else
    echo "   ❌ ANTHROPIC_API_KEY is NOT set"
    echo "   Set with: export ANTHROPIC_API_KEY='your-key'"
fi

# Check GITHUB_TOKEN
if [ -n "$GITHUB_TOKEN" ]; then
    echo "   ✅ GITHUB_TOKEN is set (${#GITHUB_TOKEN} chars)"
else
    echo "   ⚠️  GITHUB_TOKEN is NOT set (optional for some operations)"
    echo "   Set with: export GITHUB_TOKEN='your-token'"
fi

echo ""
echo "3. Testing Claude CLI with API key..."
if [ -n "$ANTHROPIC_API_KEY" ]; then
    # Try a simple headless query
    echo "   Running test query..."
    if claude -p "Say 'Hello from CI/CD'" --output-format text 2>&1 | grep -q "Hello"; then
        echo "   ✅ Claude CLI authentication successful!"
    else
        echo "   ⚠️  Claude CLI test query didn't return expected result"
        echo "   This may be normal - check logs above for details"
    fi
else
    echo "   ⏭️  Skipping test (no API key)"
fi

echo ""
echo "=================================="
echo "Verification complete!"
