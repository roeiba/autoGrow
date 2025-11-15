# Claude CLI - Headless Mode

Complete guide for using Claude Code CLI in headless mode for automation and scripting.

## 🚀 Overview

Claude Code CLI provides a powerful headless mode that allows you to:
- Run Claude programmatically without interactive UI
- Integrate Claude into scripts and automation
- Process files in batch
- Maintain multi-turn conversations
- Use JSON output for parsing

## 📦 Installation

### Install Claude Code CLI

Visit [https://code.claude.com/](https://code.claude.com/) and follow the installation instructions for your platform.

### Verify Installation

```bash
claude --version
```

## 🎯 Basic Usage

### Simple Query

```bash
# Text output (default)
claude -p "Explain this code"

# JSON output
claude -p "Explain this code" --output-format json
```

### With File Input

```bash
# Pipe file content
cat myfile.py | claude -p "Review this code"

# With output format
cat myfile.py | claude -p "Review this code" --output-format json
```

## 🔧 Configuration Options

### Output Formats

```bash
# Text output (default)
claude -p "query" --output-format text

# JSON output (for parsing)
claude -p "query" --output-format json

# Streaming JSON (for real-time updates)
claude -p "query" --output-format stream-json
```

### Tool Control

```bash
# Allow specific tools
claude -p "query" --allowedTools "Read,Write,Bash"

# Disallow specific tools
claude -p "query" --disallowedTools "Bash"

# Allow tool with specific commands
claude -p "query" --allowedTools "Bash(npm install)"
```

### Permission Modes

```bash
# Auto-accept edits
claude -p "Fix this code" --permission-mode acceptEdits

# With allowed tools
claude -p "Stage changes" \
  --allowedTools "Bash,Read" \
  --permission-mode acceptEdits
```

### System Prompts

```bash
# Append custom system prompt
claude -p "query" --append-system-prompt "You are a senior engineer"
```

### MCP Configuration

```bash
# Use MCP config file
claude -p "query" --mcp-config servers.json
```

## 🔄 Multi-turn Conversations

### Continue Last Conversation

```bash
# Continue the most recent conversation
claude --continue "Now refactor this for better performance"
```

### Resume Specific Conversation

```bash
# Resume by session ID
claude --resume 550e8400-e29b-41d4-a716-446655440000 "Update the tests"

# Resume in non-interactive mode
claude --resume <session-id> "Fix all linting issues" --no-interactive
```

## 📊 JSON Output Format

When using `--output-format json`, the response includes:

```json
{
  "type": "result",
  "subtype": "success",
  "total_cost_usd": 0.003,
  "is_error": false,
  "duration_ms": 1234,
  "duration_api_ms": 800,
  "num_turns": 6,
  "result": "The response text here...",
  "session_id": "abc123"
}
```

### Parsing JSON Output

```bash
# Extract result
result=$(claude -p "query" --output-format json)
response=$(echo "$result" | jq -r '.result')
cost=$(echo "$result" | jq -r '.total_cost_usd')
session_id=$(echo "$result" | jq -r '.session_id')

echo "Response: $response"
echo "Cost: $cost USD"
echo "Session: $session_id"
```

## 🤖 Python Integration

### Using the ClaudeAgent Class

```python
from claude_cli_agent import ClaudeAgent

# Initialize agent
agent = ClaudeAgent(output_format="json")

# Simple query
result = agent.query("What are Python best practices?")
print(result["result"])

# Code review
result = agent.code_review("myfile.py")
print(result["result"])

# Generate documentation
result = agent.generate_docs("myfile.py")
print(result["result"])

# Fix code
result = agent.fix_code("myfile.py", "Fix the memory leak")
print(result["result"])

# Continue conversation
result = agent.continue_conversation("Now add tests")
print(result["result"])
```

## 📝 Automation Scripts

### Code Review

```bash
cd scripts
./code_review_cli.sh ../src/myfile.py
```

### Generate Documentation

```bash
cd scripts
./generate_docs_cli.sh ../src
```

### Fix Code

```bash
cd scripts
./fix_code_cli.sh ../src/app.py "Fix the authentication bug"
```

### Agent Runner

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

# Resume session
./agent_runner_cli.sh resume abc123 "Update documentation"
```

## 💡 Best Practices

### 1. Use JSON Output for Parsing

```bash
# Good for automation
result=$(claude -p "Generate code" --output-format json)
code=$(echo "$result" | jq -r '.result')
cost=$(echo "$result" | jq -r '.total_cost_usd')
```

### 2. Handle Errors Gracefully

```bash
if ! claude -p "$prompt" 2>error.log; then
    echo "Error occurred:" >&2
    cat error.log >&2
    exit 1
fi
```

### 3. Use Session Management

```bash
# Save session ID for multi-turn conversations
result=$(claude -p "First query" --output-format json)
session_id=$(echo "$result" | jq -r '.session_id')

# Continue later
claude --resume "$session_id" "Follow-up query"
```

### 4. Set Timeouts

```bash
# Timeout after 5 minutes
timeout 300 claude -p "$complex_prompt" || echo "Timed out"
```

### 5. Rate Limiting

```bash
# Add delays between requests
for file in *.py; do
    claude -p "Review $file" --output-format json
    sleep 2  # 2 second delay
done
```

### 6. Control Tool Access

```bash
# Only allow safe tools
claude -p "query" --allowedTools "Read" --disallowedTools "Bash"
```

## 🔐 Security Considerations

1. **Tool Restrictions**: Use `--allowedTools` and `--disallowedTools` to control what Claude can do
2. **Permission Modes**: Be careful with `--permission-mode acceptEdits`
3. **Input Validation**: Sanitize user input before passing to Claude
4. **Output Validation**: Verify Claude's output before executing
5. **Session Management**: Protect session IDs if they contain sensitive context

## 📈 Use Cases

### 1. Automated Code Review

```bash
#!/bin/bash
for file in $(git diff --name-only main); do
    echo "Reviewing $file..."
    cat "$file" | claude -p "Review for security and quality" \
        --output-format json \
        --allowedTools "Read" \
        > "reviews/${file}.json"
done
```

### 2. Documentation Generation

```bash
#!/bin/bash
find src -name "*.py" | while read file; do
    cat "$file" | claude -p "Generate API docs" \
        --output-format json \
        > "docs/$(basename $file .py).md"
done
```

### 3. CI/CD Integration

```yaml
# .github/workflows/code-review.yml
- name: Review PR with Claude
  run: |
    git diff origin/main...HEAD | \
    claude -p "Review these changes for issues" \
      --output-format json \
      --allowedTools "Read" \
      > review.json
```

### 4. Batch Processing

```bash
#!/bin/bash
for file in src/*.py; do
    result=$(cat "$file" | claude -p "Find bugs" --output-format json)
    echo "$result" | jq -r '.result' > "reports/$(basename $file).txt"
    sleep 1
done
```

## 🆘 Troubleshooting

### Command Not Found

```bash
# Check installation
which claude

# Reinstall if needed
# Visit https://code.claude.com/
```

### JSON Parse Errors

```bash
# Verify output format
claude -p "test" --output-format json | jq '.'

# Check for errors in stderr
claude -p "test" 2>&1 | tee output.log
```

### Session Not Found

```bash
# List recent sessions (if available)
# Or start a new conversation
claude -p "Start fresh"
```

### Tool Permission Errors

```bash
# Explicitly allow tools
claude -p "query" --allowedTools "Read,Write"

# Or use permission mode
claude -p "query" --permission-mode acceptEdits
```

## 📚 Resources

- [Claude Code CLI Documentation](https://code.claude.com/docs)
- [Headless Mode Guide](https://code.claude.com/docs/en/headless)
- [CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Common Workflows](https://code.claude.com/docs/en/common-workflows)

## 🎓 Examples

See the `scripts/` directory for complete examples:
- `code_review_cli.sh` - Automated code review
- `generate_docs_cli.sh` - Documentation generation
- `fix_code_cli.sh` - Code fixing
- `agent_runner_cli.sh` - Main agent runner

See `claude_cli_agent.py` for Python integration examples.

---

**Happy Coding with Claude CLI! 🚀**
