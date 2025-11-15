# Gemini Agent - Agent Data & Configuration

This directory contains agent-specific data, scripts, and configuration for the Gemini CLI integration.

## 📁 Contents

### Setup Scripts

- **`setup_gemini_api.sh`** - Enable Google Cloud APIs and guide API key setup
- **`install_gemini_cli.sh`** - Install gemini-cli using npm or Homebrew

### Usage

#### 1. Setup Google Cloud APIs
```bash
./setup_gemini_api.sh
```

This script will:
- Check gcloud CLI installation
- Authenticate if needed
- Enable required APIs (Generative Language API, AI Platform API)
- Provide instructions for getting your API key

#### 2. Install Gemini CLI
```bash
./install_gemini_cli.sh
```

Choose your preferred installation method:
- npm (global install)
- Homebrew (macOS/Linux)
- npx (no installation)

#### 3. Configure Environment
```bash
cd ..
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

## 🔐 API Key Setup

### Get Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API Key"
3. Copy your key
4. Add to `.env` file:
   ```bash
   GEMINI_API_KEY=your-actual-api-key-here
   ```

### Authentication Options

#### Option 1: Gemini API Key (Recommended)
- Free tier: 100 requests/day
- Best for: Individual developers
- Setup: Get key from AI Studio

#### Option 2: OAuth Login
- Free tier: 60 requests/min, 1,000 requests/day
- Best for: Interactive use
- Setup: Run `gemini` and choose "Login with Google"

#### Option 3: Vertex AI
- Enterprise features
- Best for: Production workloads
- Setup: Use Google Cloud credentials

## 🛠️ Maintenance

### Update Gemini CLI
```bash
# npm
npm update -g @google/gemini-cli

# Homebrew
brew upgrade gemini-cli
```

### Check Version
```bash
gemini --version
```

### Troubleshooting

#### Command not found
```bash
# Check installation
which gemini

# Add to PATH if needed
export PATH="$PATH:$(npm config get prefix)/bin"
```

#### API Key Issues
```bash
# Verify key is set
echo $GEMINI_API_KEY

# Test with debug mode
gemini -p "test" --debug
```

## 📚 Resources

- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
- [Google AI Studio](https://aistudio.google.com/)
- [Headless Mode Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md)

## 🔄 Integration with Project

This Gemini agent integrates with the project's agentic workflow:

1. **Claude Agent** (`src/claude-agent/`) - Complex reasoning and code generation
2. **Gemini Agent** (`src/gemini-agent/`) - Fast analysis, reviews, documentation

See `examples/multi_agent_workflow.py` for integration examples.
