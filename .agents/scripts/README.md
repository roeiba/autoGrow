# AutoGrow Scripts

> **Utility scripts for local development and testing**

## Available Scripts

### 🔐 setup_secrets.sh
**Setup GitHub repository secrets**

```bash
# Set ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
./setup_secrets.sh
```

**What it does:**
- Validates API key is set
- Uses GitHub CLI to set repository secret
- Confirms successful setup

### 🚀 run_local.sh
**Run issue resolver locally**

```bash
./run_local.sh
```

**What it does:**
- Loads environment from `src/claude-agent/.env`
- Validates required variables
- Runs issue resolver with local configuration
- Shows detailed output

**Requirements:**
- `.env` file configured
- Python dependencies installed
- GitHub token with repo access

### 🔍 debug_tools.sh
**Debug agent issues**

```bash
./debug_tools.sh
```

**What it does:**
- Checks Python version
- Lists installed packages
- Verifies environment variables
- Shows git status
- Displays recent commits

**Use when:**
- Agents not working as expected
- Need to verify environment
- Troubleshooting issues

### 🧪 test_agents.sh
**Test agent functionality**

```bash
./test_agents.sh
```

**What it does:**
- Creates test issue
- Runs resolver against test issue
- Validates output
- Cleans up test data

**Use for:**
- Verifying setup
- Testing changes
- CI/CD validation

### 🔑 set_github_secrets.sh
**Batch setup all secrets**

```bash
./set_github_secrets.sh
```

**What it does:**
- Prompts for all required secrets
- Sets ANTHROPIC_API_KEY
- Sets PAT_TOKEN
- Sets optional configuration

**Interactive setup for:**
- First-time configuration
- Secret rotation
- Multiple repositories

## Usage Examples

### First Time Setup

```bash
# 1. Setup secrets
export ANTHROPIC_API_KEY="sk-ant-..."
./setup_secrets.sh

# 2. Test locally
./run_local.sh

# 3. Verify everything works
./test_agents.sh
```

### Debugging Issues

```bash
# Check environment
./debug_tools.sh

# Test specific issue
SPECIFIC_ISSUE=5 ./run_local.sh

# Run with verbose output
VERBOSE=1 ./run_local.sh
```

### Testing Changes

```bash
# Test before committing
./test_agents.sh

# Run against specific issue
./run_local.sh

# Check debug info
./debug_tools.sh
```

## Environment Variables

### Required

```bash
GITHUB_TOKEN=ghp_...           # GitHub Personal Access Token
ANTHROPIC_API_KEY=sk-ant-...   # Anthropic API Key
REPO_NAME=owner/repo           # Repository name
```

### Optional

```bash
SPECIFIC_ISSUE=5               # Target specific issue
AGENT_MODE=auto                # auto, manual, dry-run
VERBOSE=1                      # Enable verbose output
```

## Script Locations

```
.agents/scripts/
├── README.md                  # This file
├── setup_secrets.sh           # Setup GitHub secrets
├── run_local.sh               # Run resolver locally
├── debug_tools.sh             # Debug utilities
├── test_agents.sh             # Test functionality
└── set_github_secrets.sh      # Batch secret setup
```

## Common Tasks

### Setup New Repository

```bash
cd .agents/scripts
export ANTHROPIC_API_KEY="your-key"
./setup_secrets.sh
./test_agents.sh
```

### Debug Agent Failure

```bash
./debug_tools.sh              # Check environment
./run_local.sh                # Run with full output
# Check logs in output
```

### Test Before Deploy

```bash
./test_agents.sh              # Run tests
./run_local.sh                # Test locally
# Review output, then commit
```

### Rotate Secrets

```bash
# Generate new tokens
# Then update:
export ANTHROPIC_API_KEY="new-key"
./setup_secrets.sh

gh secret set PAT_TOKEN --body "new-token"
```

## Troubleshooting

### Script Not Executable

```bash
chmod +x *.sh
```

### Environment Not Loading

```bash
# Check .env file exists
ls -la ../../src/claude-agent/.env

# Verify contents (without showing secrets)
grep -v "^#" ../../src/claude-agent/.env | grep "="
```

### GitHub CLI Not Found

```bash
# Install gh CLI
brew install gh  # macOS
# or
sudo apt install gh  # Linux

# Login
gh auth login
```

### Python Dependencies Missing

```bash
# Install required packages
pip install PyGithub GitPython anthropic
```

## Security Notes

⚠️ **Never commit secrets!**

- Scripts load from `.env` (gitignored)
- Use GitHub Secrets for CI/CD
- Rotate secrets regularly
- Check `.gitignore` before committing

## See Also

- [SETUP_GUIDE.md](../docs/SETUP_GUIDE.md) - Complete setup guide
- [TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md) - Common issues
- [SECURITY_AUDIT.md](../SECURITY_AUDIT.md) - Security best practices

---

*For questions or issues, check the [documentation index](../docs/INDEX.md)*
