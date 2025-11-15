# Gemini Agent - Headless Mode Setup

This directory contains the setup and configuration for using Google's Gemini CLI in headless agent mode for automated AI workflows.

## 🚀 Quick Start

### 1. Prerequisites

- Node.js version 20 or higher
- gcloud CLI installed and configured
- A Google Cloud Project with billing enabled

### 2. Setup API Key

Run the setup script to enable required APIs:

```bash
cd src/gemini-agent
./.agents/setup_gemini_api.sh
```

Then get your API key from [Google AI Studio](https://aistudio.google.com/apikey) and add it to your environment:

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your-actual-api-key-here
```

### 3. Install Gemini CLI

Choose one of the following installation methods:

```bash
# Option 1: Install globally with npm
npm install -g @google/gemini-cli

# Option 2: Install with Homebrew (macOS/Linux)
brew install gemini-cli

# Option 3: Run with npx (no installation)
npx @google/gemini-cli
```

### 4. Test the Setup

```bash
# Load environment variables
source .env

# Test with a simple prompt
gemini -p "Hello, what can you help me with?" --output-format json
```

## 🤖 Agent Mode Usage

The gemini-cli in headless mode is perfect for automation and scripting. Here are the key features:

### Basic Headless Commands

```bash
# Simple prompt
gemini -p "Explain this code" --output-format json

# With file input
cat file.py | gemini -p "Review this code" --output-format json

# With auto-approval (YOLO mode)
gemini -p "Fix bugs in this code" --yolo --output-format json

# Specify model
gemini -p "Complex task" -m gemini-2.5-pro --output-format json
```

### Key Options for Agent Mode

| Option | Description | Example |
|--------|-------------|---------|
| `--prompt`, `-p` | Run in headless mode | `gemini -p "query"` |
| `--output-format` | Output format (text, json) | `--output-format json` |
| `--model`, `-m` | Specify Gemini model | `-m gemini-2.5-flash` |
| `--yolo`, `-y` | Auto-approve all actions | `--yolo` |
| `--approval-mode` | Set approval mode | `--approval-mode auto_edit` |
| `--include-directories` | Include additional dirs | `--include-directories src,docs` |
| `--debug`, `-d` | Enable debug mode | `--debug` |

## 📝 Example Scripts

See the `scripts/` directory for example automation scripts:

- `code_review.sh` - Automated code review
- `generate_docs.sh` - Generate documentation
- `analyze_logs.sh` - Log analysis
- `batch_process.sh` - Batch file processing

## 🔐 Authentication Options

### Option 1: Gemini API Key (Recommended for this setup)
- Free tier: 100 requests/day with Gemini 2.5 Pro
- Get key from: https://aistudio.google.com/apikey
- Set: `export GEMINI_API_KEY="your-key"`

### Option 2: OAuth Login
- Free tier: 60 requests/min, 1,000 requests/day
- Run: `gemini` (interactive mode) and choose "Login with Google"

### Option 3: Vertex AI
- Enterprise features with billing
- Set: `export GOOGLE_API_KEY="your-key"` and `export GOOGLE_GENAI_USE_VERTEXAI=true`

## 📚 Resources

- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
- [Headless Mode Documentation](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md)
- [Configuration Guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/configuration.md)
- [Google AI Studio](https://aistudio.google.com/)

## 🛠️ Troubleshooting

### API Key Issues
```bash
# Verify API key is set
echo $GEMINI_API_KEY

# Test API key
gemini -p "test" --debug
```

### Rate Limits
- Free tier: 100 requests/day
- Upgrade at: https://aistudio.google.com/

### Model Selection
```bash
# Use faster model for simple tasks
gemini -p "simple query" -m gemini-2.5-flash

# Use pro model for complex tasks
gemini -p "complex analysis" -m gemini-2.5-pro
```

## 📁 Project Structure

```
gemini-agent/
├── .agents/
│   └── setup_gemini_api.sh    # API setup script
├── scripts/
│   ├── code_review.sh          # Code review automation
│   ├── generate_docs.sh        # Documentation generation
│   ├── analyze_logs.sh         # Log analysis
│   └── batch_process.sh        # Batch processing
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```
