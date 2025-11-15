# Gemini Agent - Quick Start Guide

Get up and running with Gemini CLI in agent mode in 5 minutes.

## ⚡ Quick Setup (5 minutes)

### Step 1: Get Your API Key (2 minutes)

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API Key"
3. Copy your API key

### Step 2: Configure Environment (1 minute)

```bash
cd src/gemini-agent

# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# Replace 'your-api-key-here' with your actual key
echo 'GEMINI_API_KEY=your-actual-api-key-here' > .env
```

### Step 3: Install Gemini CLI (2 minutes)

Choose one method:

```bash
# Option 1: npm (recommended)
npm install -g @google/gemini-cli

# Option 2: Homebrew (macOS/Linux)
brew install gemini-cli

# Option 3: npx (no installation)
# Just use 'npx @google/gemini-cli' instead of 'gemini'
```

Verify installation:
```bash
gemini --version
```

### Step 4: Test It! (30 seconds)

```bash
# Load your API key
source .env

# Test with a simple query
gemini -p "Hello! Can you help me with code?" --output-format json
```

✅ If you see a JSON response, you're all set!

## 🚀 Using Agent Mode

### Interactive Mode
```bash
# Start interactive chat
gemini
```

### Headless Mode (Agent Mode)
```bash
# Simple query
gemini -p "Explain this project structure" --output-format json

# With file input
cat myfile.py | gemini -p "Review this code" --output-format json

# Auto-approve actions (YOLO mode)
gemini -p "Fix bugs in this code" --yolo --output-format json
```

## 📝 Quick Examples

### 1. Code Review
```bash
cd scripts
./code_review.sh ../../src/agentic_workflow.py
```

### 2. Generate Documentation
```bash
cd scripts
./generate_docs.sh ../../src
```

### 3. Custom Agent Task
```bash
cd scripts
./agent_runner.sh custom "Analyze the project and suggest improvements"
```

### 4. Python Integration
```bash
# Review a file
python gemini_agent.py ../agentic_workflow.py

# Or use in your code
python -c "
from gemini_agent import GeminiAgent
agent = GeminiAgent()
result = agent.query('What is Python?')
print(result['response'])
"
```

## 🎯 Common Use Cases

### Automated Code Review
```bash
# Review all Python files in a directory
./scripts/batch_process.sh ../src "Review this code for security issues"
```

### Log Analysis
```bash
# Analyze application logs
./scripts/analyze_logs.sh /path/to/app.log
```

### Documentation Generation
```bash
# Generate docs for entire project
./scripts/generate_docs.sh ../..
```

### CI/CD Integration
```bash
# In your CI pipeline
export GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}
gemini -p "Review these changes" --output-format json < git_diff.txt
```

## 🔧 Configuration

### Environment Variables
```bash
# Required
export GEMINI_API_KEY="your-key"

# Optional
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_GENAI_USE_VERTEXAI=true  # For Vertex AI
```

### Model Selection
```bash
# Fast model for simple tasks
gemini -p "query" -m gemini-2.5-flash

# Pro model for complex tasks
gemini -p "complex query" -m gemini-2.5-pro
```

### Output Formats
```bash
# JSON output (for parsing)
gemini -p "query" --output-format json

# Text output (for reading)
gemini -p "query" --output-format text
```

## 📊 Rate Limits

### Free Tier (Gemini API Key)
- 100 requests per day
- Gemini 2.5 Pro model
- 1M token context window

### Upgrade Options
- Visit [Google AI Studio](https://aistudio.google.com/) for paid tiers
- Or use Vertex AI for enterprise features

## ❓ Troubleshooting

### "GEMINI_API_KEY not set"
```bash
# Make sure you've sourced the .env file
source .env

# Or export it directly
export GEMINI_API_KEY="your-key"
```

### "gemini: command not found"
```bash
# Install gemini-cli
npm install -g @google/gemini-cli

# Or use npx
npx @google/gemini-cli -p "test"
```

### Rate Limit Errors
```bash
# Use flash model for faster/cheaper requests
gemini -p "query" -m gemini-2.5-flash

# Add delays in batch processing
sleep 2  # between requests
```

### API Key Invalid
1. Check your key at [Google AI Studio](https://aistudio.google.com/apikey)
2. Make sure there are no extra spaces or quotes
3. Regenerate if necessary

## 🎓 Next Steps

1. **Explore Scripts**: Check out `scripts/` for more examples
2. **Read Docs**: See `README.md` for detailed documentation
3. **Python Integration**: Use `gemini_agent.py` in your Python projects
4. **Customize**: Modify scripts for your specific use cases

## 📚 Resources

- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
- [Headless Mode Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md)
- [Google AI Studio](https://aistudio.google.com/)
- [API Documentation](https://ai.google.dev/docs)

## 💡 Pro Tips

1. **Use JSON output** for automation and parsing
2. **Choose the right model**: Flash for speed, Pro for quality
3. **Include context**: Use `--include-directories` for better results
4. **Batch processing**: Add delays to avoid rate limits
5. **YOLO mode**: Use `--yolo` only when you trust the changes

---

**Need help?** Check the main [README.md](README.md) or open an issue.
