#!/bin/bash

# Setup Gemini API Key for gemini-cli
# This script creates a Gemini API key using gcloud CLI

set -e

echo "🔐 Setting up Gemini API Key..."
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed."
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo "⚠️  You are not authenticated with gcloud."
    echo "Running: gcloud auth login"
    gcloud auth login
fi

# Get current project
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)

if [ -z "$CURRENT_PROJECT" ]; then
    echo "⚠️  No default project set."
    echo "Available projects:"
    gcloud projects list --format="table(projectId,name)"
    echo ""
    read -p "Enter your Google Cloud Project ID: " PROJECT_ID
    gcloud config set project "$PROJECT_ID"
    CURRENT_PROJECT="$PROJECT_ID"
else
    echo "📦 Current project: $CURRENT_PROJECT"
    read -p "Use this project? (y/n): " USE_CURRENT
    if [[ "$USE_CURRENT" != "y" ]]; then
        echo "Available projects:"
        gcloud projects list --format="table(projectId,name)"
        echo ""
        read -p "Enter your Google Cloud Project ID: " PROJECT_ID
        gcloud config set project "$PROJECT_ID"
        CURRENT_PROJECT="$PROJECT_ID"
    fi
fi

echo ""
echo "🔧 Enabling required APIs..."

# Enable Generative Language API (for Gemini API)
gcloud services enable generativelanguage.googleapis.com --project="$CURRENT_PROJECT" 2>/dev/null || true

# Enable AI Platform API (for Vertex AI if needed)
gcloud services enable aiplatform.googleapis.com --project="$CURRENT_PROJECT" 2>/dev/null || true

echo ""
echo "✅ APIs enabled successfully!"
echo ""
echo "📝 To get your Gemini API key, visit:"
echo "   https://aistudio.google.com/apikey"
echo ""
echo "🔑 Once you have your API key, add it to your environment:"
echo ""
echo "   export GEMINI_API_KEY=\"your-api-key-here\""
echo ""
echo "   Or add it to your ~/.zshrc or ~/.bashrc:"
echo "   echo 'export GEMINI_API_KEY=\"your-api-key-here\"' >> ~/.zshrc"
echo ""
echo "💡 For this project, you can also create a .env file:"
echo "   echo 'GEMINI_API_KEY=your-api-key-here' > .env"
echo ""
echo "🚀 After setting the API key, you can use gemini-cli in headless mode:"
echo "   gemini -p \"your prompt here\" --output-format json"
echo ""
