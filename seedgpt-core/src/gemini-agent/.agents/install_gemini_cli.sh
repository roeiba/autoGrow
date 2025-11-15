#!/bin/bash

# Install Gemini CLI
# This script installs gemini-cli using the best available method

set -e

echo "🚀 Installing Gemini CLI..."
echo ""

# Check Node.js version
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    echo "📦 Node.js version: $(node --version)"
    
    if [ "$NODE_VERSION" -lt 20 ]; then
        echo "⚠️  Warning: Node.js version 20 or higher is recommended"
        echo "   Current version: $(node --version)"
        echo "   Install from: https://nodejs.org/"
        echo ""
    fi
else
    echo "❌ Error: Node.js is not installed"
    echo "Please install Node.js 20+ from: https://nodejs.org/"
    exit 1
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed"
    echo "Please install npm (comes with Node.js)"
    exit 1
fi

# Check if gemini-cli is already installed
if command -v gemini &> /dev/null; then
    CURRENT_VERSION=$(gemini --version 2>&1 || echo "unknown")
    echo "✅ Gemini CLI is already installed: $CURRENT_VERSION"
    echo ""
    read -p "Reinstall/update? (y/n): " REINSTALL
    if [[ "$REINSTALL" != "y" ]]; then
        echo "Skipping installation"
        exit 0
    fi
fi

echo ""
echo "Choose installation method:"
echo "  1) npm (global install - recommended)"
echo "  2) Homebrew (macOS/Linux)"
echo "  3) Skip (use npx instead)"
echo ""
read -p "Enter choice (1-3): " CHOICE

case $CHOICE in
    1)
        echo ""
        echo "📦 Installing with npm..."
        npm install -g @google/gemini-cli
        
        if command -v gemini &> /dev/null; then
            echo ""
            echo "✅ Successfully installed!"
            echo "   Version: $(gemini --version)"
        else
            echo ""
            echo "⚠️  Installation completed but 'gemini' command not found"
            echo "   You may need to add npm global bin to your PATH"
            echo "   Run: npm config get prefix"
            echo "   Then add <prefix>/bin to your PATH"
        fi
        ;;
    
    2)
        if ! command -v brew &> /dev/null; then
            echo "❌ Error: Homebrew is not installed"
            echo "Install from: https://brew.sh/"
            exit 1
        fi
        
        echo ""
        echo "🍺 Installing with Homebrew..."
        brew install gemini-cli
        
        if command -v gemini &> /dev/null; then
            echo ""
            echo "✅ Successfully installed!"
            echo "   Version: $(gemini --version)"
        else
            echo ""
            echo "❌ Installation failed"
            exit 1
        fi
        ;;
    
    3)
        echo ""
        echo "📝 Skipping installation"
        echo ""
        echo "You can use gemini-cli with npx (no installation needed):"
        echo "   npx @google/gemini-cli -p \"your prompt\""
        echo ""
        echo "Or install it later with:"
        echo "   npm install -g @google/gemini-cli"
        exit 0
        ;;
    
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "=" * 50
echo "🎉 Gemini CLI Setup Complete!"
echo "=" * 50
echo ""
echo "Next steps:"
echo "  1. Get your API key from: https://aistudio.google.com/apikey"
echo "  2. Add it to .env file:"
echo "     cd $(dirname $0)/.."
echo "     echo 'GEMINI_API_KEY=your-key-here' > .env"
echo ""
echo "  3. Test it:"
echo "     source .env"
echo "     gemini -p \"Hello!\" --output-format json"
echo ""
echo "  4. See QUICKSTART.md for more examples"
echo ""
