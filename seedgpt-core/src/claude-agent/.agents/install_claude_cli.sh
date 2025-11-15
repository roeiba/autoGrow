#!/bin/bash

# Install Claude Code CLI
# This script helps install Claude Code CLI on macOS

set -e

echo "🤖 Claude Code CLI Installation Script"
echo "========================================"
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  This script is designed for macOS"
    echo "For other platforms, visit: https://code.claude.com/"
    exit 1
fi

echo "📋 Installation Options:"
echo ""
echo "Claude Code CLI is distributed as a desktop application."
echo "You need to download and install it from the official website."
echo ""
echo "🌐 Visit: https://code.claude.com/"
echo ""
echo "After installation, the 'claude' command will be available in your terminal."
echo ""
echo "Installation steps:"
echo "1. Visit https://code.claude.com/"
echo "2. Download Claude Code for macOS"
echo "3. Install the application"
echo "4. Open Claude Code at least once"
echo "5. The CLI will be automatically available"
echo ""

# Check if Homebrew is available (in case there's a brew formula)
if command -v brew &> /dev/null; then
    echo "✅ Homebrew detected"
    echo ""
    echo "Note: Claude Code CLI is typically installed via the desktop app,"
    echo "but you can check for brew cask availability:"
    echo ""
    echo "  brew search claude"
    echo ""
fi

echo "After installation, verify with:"
echo "  claude --version"
echo ""
echo "Then test with:"
echo "  claude -p \"Hello, Claude!\""
echo ""

# Offer to open the website
read -p "Would you like to open the Claude Code website now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Opening https://code.claude.com/ ..."
    open "https://code.claude.com/"
fi

echo ""
echo "📚 After installation, see:"
echo "  - CLAUDE_CLI_QUICKSTART.md for quick start"
echo "  - CLAUDE_CLI_HEADLESS.md for complete documentation"
