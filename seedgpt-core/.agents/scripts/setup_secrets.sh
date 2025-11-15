#!/bin/bash
# Script to securely set ANTHROPIC_API_KEY as GitHub Actions secret


if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ No API key provided. Exiting."
    exit 1
fi

echo ""
echo "Setting secret in repository: roeiba/seedgpt"

# Set the secret using gh CLI
echo "$ANTHROPIC_API_KEY" | gh secret set ANTHROPIC_API_KEY --repo roeiba/seedgpt

if [ $? -eq 0 ]; then
    echo "✅ ANTHROPIC_API_KEY secret set successfully!"
    echo ""
    echo "You can verify it at:"
    echo "https://github.com/roeiba/seedgpt/settings/secrets/actions"
else
    echo "❌ Failed to set secret"
    exit 1
fi
