# Claude Agent Executor

An autonomous agent that uses Claude AI to automatically fix GitHub issues and create pull requests. Now with **Claude Code CLI headless mode** support!

## 🎯 Two Modes Available

### 1. Docker-Based Agent (Original)
- Autonomous issue resolution using Claude API
- GitHub CLI integration
- Fully containerized
- Automatic PR creation

### 2. Claude CLI Headless Mode (NEW!)
- Use Claude Code CLI in headless mode
- Scriptable automation
- Python wrapper available
- Multi-turn conversations
- Session management

## Features

### Docker-Based Agent
- 🤖 Autonomous issue resolution using Claude AI
- 🔧 GitHub CLI integration for seamless repo interaction
- 🐳 Fully containerized for consistent execution
- 🔐 Secure credential management via environment variables
- 📝 Automatic PR creation with detailed descriptions
- 🎨 **Customizable prompts** - Use built-in templates or create your own
- 📚 Multiple prompt templates (default, minimal, detailed)
- 🔧 External prompt files for complete customization

### Claude CLI Headless Mode (NEW!)
- 🚀 **Headless automation** - Run Claude programmatically
- 📝 **Code review** - Automated security and quality checks
- 📚 **Documentation** - Generate comprehensive docs
- 🔧 **Code fixing** - Fix issues with AI assistance
- 🔄 **Multi-turn** - Maintain conversation context
- 🐍 **Python wrapper** - Easy integration
- 📊 **JSON output** - Parse results programmatically

## Prerequisites

### For Docker-Based Agent
- Docker and Docker Compose installed
- GitHub Personal Access Token with repo permissions
- Anthropic API Key

### For Claude CLI Headless Mode
- Claude Code CLI installed ([https://code.claude.com/](https://code.claude.com/))
- Python 3.8+ (for Python wrapper)

## Quick Start

### Option A: Docker-Based Agent

#### 1. Setup Environment

Copy the example environment file and configure your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
- `GITHUB_TOKEN`: Your GitHub Personal Access Token
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `REPO_URL`: The GitHub repository URL to work on
- `ISSUE_NUMBER`: (Optional) Specific issue number, or leave empty for auto-selection

#### 2. Build the Docker Image

```bash
docker-compose build
```

#### 3. Run the Agent

```bash
docker-compose up
```

The agent will:
1. Authenticate with GitHub
2. Clone the specified repository
3. Select an issue (or use the provided issue number)
4. Analyze the issue and implement a fix
5. Create a new branch
6. Commit the changes
7. Push the branch
8. Create a pull request

### Option B: Claude CLI Headless Mode (NEW!)

#### 1. Install Claude Code CLI

Visit [https://code.claude.com/](https://code.claude.com/) and follow installation instructions.

#### 2. Verify Installation

```bash
claude --version
```

#### 3. Run Automation Scripts

```bash
cd scripts

# Code review
./code_review_cli.sh ../src/myfile.py

# Generate documentation
./generate_docs_cli.sh ../src

# Fix code
./fix_code_cli.sh ../src/app.py "Fix the authentication bug"

# Agent runner
./agent_runner_cli.sh code-review ../src
```

#### 4. Python Integration

```python
from claude_cli_agent import ClaudeAgent

# Initialize
agent = ClaudeAgent()

# Code review
result = agent.code_review("myfile.py")
print(result["result"])

# Generate docs
result = agent.generate_docs("myfile.py")
print(result["result"])
```

**📚 See [CLAUDE_CLI_QUICKSTART.md](CLAUDE_CLI_QUICKSTART.md) for complete guide**

## Manual Docker Run

If you prefer to run without docker-compose:

```bash
docker build -t claude-agent .

docker run --rm \
  -e GITHUB_TOKEN="your_token" \
  -e ANTHROPIC_API_KEY="your_api_key" \
  -e REPO_URL="https://github.com/owner/repo" \
  -e ISSUE_NUMBER="123" \
  claude-agent
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Yes | GitHub Personal Access Token with repo access |
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude |
| `REPO_URL` | Yes | Full GitHub repository URL |
| `ISSUE_NUMBER` | No | Specific issue to fix (auto-selects if empty) |
| `AGENT_MODE` | No | Execution mode: `auto`, `manual`, `dry-run` (default: `auto`) |
| `PROMPT_TEMPLATE` | No | Prompt template: `default`, `minimal`, `detailed`, or path to custom file |

### GitHub Token Permissions

Your GitHub token needs the following scopes:
- `repo` (Full control of private repositories)
- `workflow` (if working with GitHub Actions)

Create a token at: https://github.com/settings/tokens

### Anthropic API Key

Get your API key from: https://console.anthropic.com/

## Architecture

```
claude-agent/
├── Dockerfile              # Container definition
├── docker-compose.yml      # Orchestration config
├── .env.example           # Environment template
├── scripts/
│   ├── entrypoint.sh      # Container entry point
│   ├── agent-workflow.sh  # Main agent logic
│   └── fallback-agent.sh  # Fallback when CLI unavailable
└── README.md              # This file
```

## Workflow

1. **Authentication**: Validates GitHub and Anthropic credentials
2. **Repository Setup**: Clones the target repository
3. **Issue Selection**: Auto-selects or uses provided issue number
4. **Analysis**: Claude analyzes the codebase and issue
5. **Implementation**: Agent implements the fix
6. **Quality Check**: Validates changes
7. **PR Creation**: Creates pull request with detailed description

## Troubleshooting

### Claude CLI Not Found

If `claude-code` CLI is not available, the agent will use a fallback mode. To properly integrate:

1. Check the official claude-code CLI installation method
2. Update the Dockerfile with correct installation commands
3. Adjust the CLI invocation in `agent-workflow.sh`

### Authentication Failures

- Verify your GitHub token has correct permissions
- Check that the Anthropic API key is valid
- Ensure tokens are properly set in `.env` file

### No Issues Found

If the agent reports no open issues:
- Verify the repository has open issues
- Check that your GitHub token has access to the repository
- Manually specify an issue number via `ISSUE_NUMBER`

## Customizing Prompts

The agent supports customizable prompts for different use cases:

### Using Built-in Templates

```bash
# Use detailed template for complex issues
export PROMPT_TEMPLATE=detailed

# Use minimal template for simple fixes
export PROMPT_TEMPLATE=minimal

# Use default template (balanced)
export PROMPT_TEMPLATE=default
```

### Using Custom Prompts

```bash
# Create your custom prompt
cat > my-prompt.txt << 'EOF'
Fix issue #{issue_number}: {issue_title}

{issue_body}

Repository: {repo_owner}/{repo_name}
Languages: {languages}

Provide JSON with files_to_modify array.
EOF

# Use it
export PROMPT_TEMPLATE=/path/to/my-prompt.txt
./run-agent.sh
```

### Available Templates

- **default.txt**: Balanced template for general use
- **minimal.txt**: Concise template for simple fixes
- **detailed.txt**: Comprehensive template for complex issues

See [CUSTOM_PROMPTS.md](./CUSTOM_PROMPTS.md) for complete guide.

## Advanced Usage

### Running Multiple Agents

You can run multiple instances for different repositories:

```bash
# Terminal 1
REPO_URL=https://github.com/owner/repo1 docker-compose up

# Terminal 2
REPO_URL=https://github.com/owner/repo2 docker-compose up
```

### Custom Branch Naming

Edit `agent-workflow.sh` to customize the branch naming pattern:

```bash
BRANCH_NAME="fix/issue-${ISSUE_NUMBER}-$(date +%s)"
```

### Integration with CI/CD

The agent can be triggered from CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Claude Agent
  run: |
    docker run --rm \
      -e GITHUB_TOKEN="${{ secrets.GITHUB_TOKEN }}" \
      -e ANTHROPIC_API_KEY="${{ secrets.ANTHROPIC_API_KEY }}" \
      -e REPO_URL="${{ github.repository }}" \
      claude-agent
```

## Security Considerations

- Never commit `.env` file with real credentials
- Use secrets management in production (e.g., AWS Secrets Manager, HashiCorp Vault)
- Rotate API keys regularly
- Review agent-generated PRs before merging
- Consider running in isolated networks

## Future Enhancements

- [ ] Support for multiple AI providers (OpenAI, Gemini, etc.)
- [ ] Webhook integration for automatic triggering
- [ ] Issue priority and label filtering
- [ ] Multi-issue batch processing
- [ ] Testing framework integration
- [ ] Slack/Discord notifications
- [ ] Metrics and logging dashboard

## License

Part of the AI Project Template. See main repository for license details.
