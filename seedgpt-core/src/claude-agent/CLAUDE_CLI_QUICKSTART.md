# Claude CLI - Quick Start Guide

Get up and running with Claude Code CLI in headless mode in 5 minutes.

## ⚡ Quick Setup (5 minutes)

### Step 1: Install Claude Code CLI (2 minutes)

Visit [https://code.claude.com/](https://code.claude.com/) and follow the installation instructions for your platform.

### Step 2: Verify Installation (30 seconds)

```bash
claude --version
```

### Step 3: Test It! (30 seconds)

```bash
# Simple query
claude -p "Hello! Can you help me with code?"

# JSON output
claude -p "What are Python best practices?" --output-format json
```

✅ If you see a response, you're all set!

## 🚀 Using Headless Mode

### Basic Commands

```bash
# Simple query
claude -p "Explain this project structure"

# With file input
cat myfile.py | claude -p "Review this code"

# JSON output for parsing
claude -p "Generate code" --output-format json

# With tool restrictions
claude -p "Fix this code" --allowedTools "Read,Write"
```

### Multi-turn Conversations

```bash
# Continue last conversation
claude --continue "Now add tests"

# Resume specific conversation
claude --resume <session-id> "Update documentation"
```

## 📝 Quick Examples

### 1. Code Review

```bash
cd scripts
./code_review_cli.sh ../src/myfile.py
```

### 2. Generate Documentation

```bash
cd scripts
./generate_docs_cli.sh ../src
```

### 3. Fix Code

```bash
cd scripts
./fix_code_cli.sh ../src/app.py "Fix the authentication bug"
```

### 4. Python Integration

```python
from claude_cli_agent import ClaudeAgent

# Initialize agent
agent = ClaudeAgent()

# Code review
result = agent.code_review("myfile.py")
print(result["result"])

# Generate docs
result = agent.generate_docs("myfile.py")
print(result["result"])

# Fix code
result = agent.fix_code("myfile.py", "Fix memory leak")
print(result["result"])
```

### 5. Agent Runner

```bash
cd scripts

# Code review
./agent_runner_cli.sh code-review ../src/app.py

# Generate docs
./agent_runner_cli.sh generate-docs ../src

# Fix code
./agent_runner_cli.sh fix-code app.py "Fix memory leak"

# Custom prompt
./agent_runner_cli.sh custom "Analyze the project structure"

# Continue conversation
./agent_runner_cli.sh continue "Now add tests"
```

## 🎯 Common Use Cases

### Automated Code Review

```bash
# Review all Python files
for file in src/*.py; do
    cat "$file" | claude -p "Review for security issues" \
        --output-format json \
        > "reviews/$(basename $file).json"
done
```

### Documentation Generation

```bash
# Generate docs for all files
find src -name "*.py" | while read file; do
    cat "$file" | claude -p "Generate API docs" \
        --output-format json \
        > "docs/$(basename $file .py).md"
done
```

### CI/CD Integration

```bash
# In your CI pipeline
git diff origin/main...HEAD | \
claude -p "Review these changes" \
  --output-format json \
  --allowedTools "Read" \
  > review.json
```

## 🔧 Configuration

### Output Formats

```bash
# Text (default)
claude -p "query"

# JSON (for parsing)
claude -p "query" --output-format json

# Streaming JSON (real-time)
claude -p "query" --output-format stream-json
```

### Tool Control

```bash
# Allow specific tools
claude -p "query" --allowedTools "Read,Write"

# Disallow tools
claude -p "query" --disallowedTools "Bash"

# Permission mode
claude -p "Fix code" --permission-mode acceptEdits
```

### System Prompts

```bash
# Add custom instructions
claude -p "query" --append-system-prompt "You are a senior engineer"
```

## 💡 Pro Tips

1. **Use JSON output** for automation and parsing
2. **Control tool access** with `--allowedTools` and `--disallowedTools`
3. **Session management** for multi-turn conversations
4. **Add delays** between requests to avoid rate limits
5. **Handle errors** gracefully in scripts

## 📊 JSON Output

When using `--output-format json`, you get:

```json
{
  "type": "result",
  "subtype": "success",
  "total_cost_usd": 0.003,
  "duration_ms": 1234,
  "result": "The response text here...",
  "session_id": "abc123"
}
```

Parse with `jq`:

```bash
result=$(claude -p "query" --output-format json)
response=$(echo "$result" | jq -r '.result')
cost=$(echo "$result" | jq -r '.total_cost_usd')
session=$(echo "$result" | jq -r '.session_id')
```

## ❓ Troubleshooting

### "claude: command not found"

```bash
# Check installation
which claude

# Reinstall from https://code.claude.com/
```

### JSON Parse Errors

```bash
# Verify JSON output
claude -p "test" --output-format json | jq '.'

# Check stderr for errors
claude -p "test" 2>&1 | tee output.log
```

### Tool Permission Errors

```bash
# Explicitly allow tools
claude -p "query" --allowedTools "Read,Write"

# Or use permission mode
claude -p "query" --permission-mode acceptEdits
```

## 🎓 Next Steps

1. **Explore Scripts**: Check out `scripts/` for more examples
2. **Read Docs**: See `CLAUDE_CLI_HEADLESS.md` for detailed documentation
3. **Python Integration**: Use `claude_cli_agent.py` in your Python projects
4. **Customize**: Modify scripts for your specific use cases

## 📚 Resources

- [Claude Code CLI Documentation](https://code.claude.com/docs)
- [Headless Mode Guide](https://code.claude.com/docs/en/headless)
- [CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Common Workflows](https://code.claude.com/docs/en/common-workflows)

## 💬 Examples in This Project

- **Scripts**: `scripts/code_review_cli.sh`, `generate_docs_cli.sh`, `fix_code_cli.sh`
- **Python**: `claude_cli_agent.py`
- **Tests**: `tests/unit/test_claude_cli_agent.py`
- **Documentation**: `CLAUDE_CLI_HEADLESS.md`

---

**Need help?** Check the full [CLAUDE_CLI_HEADLESS.md](CLAUDE_CLI_HEADLESS.md) documentation.

**Happy Coding with Claude CLI! 🚀**
