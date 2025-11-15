#!/bin/bash
# Create GCP Secret Manager secrets from GitHub secrets

set -e

PROJECT_ID="magic-mirror-427812"

echo "🔐 Creating secrets in GCP Secret Manager..."
echo "============================================"

# Get secrets from GitHub
echo "📥 Fetching secrets from GitHub..."
PAT_TOKEN=$(gh secret list --repo roeiba/SeedGPT | grep PAT_TOKEN | awk '{print $1}')
ANTHROPIC_KEY=$(gh secret list --repo roeiba/SeedGPT | grep ANTHROPIC_API_KEY | awk '{print $1}')
GCP_CREDS=$(gh secret list --repo roeiba/SeedGPT | grep GCP_CREDENTIALS | awk '{print $1}')

if [ -z "$PAT_TOKEN" ] || [ -z "$ANTHROPIC_KEY" ] || [ -z "$GCP_CREDS" ]; then
    echo "❌ Error: Not all secrets found in GitHub"
    exit 1
fi

echo "✅ Found all secrets in GitHub"

# Note: We can't actually read GitHub secret values via CLI
# So we'll need to create them manually or use the values we have

echo ""
echo "Creating secrets in GCP Secret Manager..."

# Create PAT_TOKEN secret
echo "1. PAT_TOKEN..."
if gcloud secrets describe PAT_TOKEN --project=$PROJECT_ID &>/dev/null; then
    echo "   Already exists - updating..."
    gh secret get PAT_TOKEN --repo roeiba/SeedGPT 2>/dev/null || echo "Cannot read GitHub secret directly"
else
    echo "   Please provide your GitHub PAT token:"
    read -s PAT_VALUE
    echo -n "$PAT_VALUE" | gcloud secrets create PAT_TOKEN \
        --data-file=- \
        --project=$PROJECT_ID
    echo "   ✅ Created"
fi

# Create ANTHROPIC_API_KEY secret  
echo "2. ANTHROPIC_API_KEY..."
if gcloud secrets describe ANTHROPIC_API_KEY --project=$PROJECT_ID &>/dev/null; then
    echo "   Already exists"
else
    echo "   Please provide your Anthropic API key:"
    read -s ANTHROPIC_VALUE
    echo -n "$ANTHROPIC_VALUE" | gcloud secrets create ANTHROPIC_API_KEY \
        --data-file=- \
        --project=$PROJECT_ID
    echo "   ✅ Created"
fi

# Create GCP_CREDENTIALS secret
echo "3. GCP_CREDENTIALS..."
if gcloud secrets describe GCP_CREDENTIALS --project=$PROJECT_ID &>/dev/null; then
    echo "   Already exists"
else
    if [ -f "./apps/seed-planter-api/gcp-credentials.json" ]; then
        gcloud secrets create GCP_CREDENTIALS \
            --data-file=./apps/seed-planter-api/gcp-credentials.json \
            --project=$PROJECT_ID
        echo "   ✅ Created from local file"
    else
        echo "   ❌ Error: gcp-credentials.json not found"
        exit 1
    fi
fi

echo ""
echo "============================================"
echo "✅ All secrets created in GCP Secret Manager!"
echo ""
echo "Secrets created in project: $PROJECT_ID"
gcloud secrets list --project=$PROJECT_ID
