# AutoGrow Setup Guide

> **Complete guide to setting up your AutoGrow instance**

## Prerequisites

- GitHub account
- Anthropic API key ([Get one here](https://console.anthropic.com))
- Git installed locally
- GitHub CLI (`gh`) installed (optional but recommended)

## Quick Setup (4 Steps)

### Step 1: Fork the Repository

```bash
# On GitHub, click "Fork" button
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/autoGrow.git
cd autoGrow
```

### Step 2: Configure Secrets

#### Option A: Using GitHub CLI (Recommended)

```bash
# Set Anthropic API key
gh secret set ANTHROPIC_API_KEY --body "sk-ant-your-key-here"

# Set GitHub Personal Access Token
gh secret set PAT_TOKEN --body "ghp_your-token-here"
```

#### Option B: Via GitHub Web Interface

1. Go to: `Settings → Secrets and variables → Actions`
2. Click "New repository secret"
3. Add:
   - Name: `ANTHROPIC_API_KEY`, Value: `sk-ant-...`
   - Name: `PAT_TOKEN`, Value: `ghp_...`

#### Option C: Using Setup Script

```bash
# From the .agents/scripts directory
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
./scripts/setup_secrets.sh
```

### Step 3: Update PROJECT_BRIEF.md

Edit `PROJECT_BRIEF.md` with your project vision:

```markdown
# My Awesome Project

## Vision
Build an AI-powered task management system...

## Core Requirements
- User authentication
- Task CRUD operations
- AI-powered task suggestions
...
```

### Step 4: Commit & Push

```bash
git add PROJECT_BRIEF.md
git commit -m "Initialize my AutoGrow project"
git push
```

**That's it!** 🎉 Your project will start growing automatically.

## What Happens Next

Within 10-20 minutes:

1. ✅ **Issue Generator** creates 3 improvement issues
2. ✅ **Issue Resolver** picks an issue and writes code
3. ✅ **Pull Request** created with the solution
4. ✅ **QA Agent** monitors project health

Check:
- **Issues tab** - New issues appear
- **Pull Requests tab** - AI-generated code
- **Actions tab** - Watch agents work

## Verification

### Check Secrets Are Set

```bash
gh secret list
```

Should show:
```
ANTHROPIC_API_KEY  Updated YYYY-MM-DD
PAT_TOKEN          Updated YYYY-MM-DD
```

### Check Workflows Are Enabled

```bash
gh workflow list
```

Should show:
```
Issue Generator Agent    active
Issue Resolver Agent     active
QA Agent                 active
```

### Trigger Manual Run

```bash
# Test issue generator
gh workflow run issue-generator.yml

# Test issue resolver
gh workflow run issue-resolver.yml

# Test QA agent
gh workflow run qa-agent.yml
```

## Configuration Options

### Adjust Agent Frequency

Edit workflow files in `.github/workflows/`:

```yaml
# Issue Generator - every 10 minutes (default)
schedule:
  - cron: '*/10 * * * *'

# Issue Resolver - every 10 minutes (default)
schedule:
  - cron: '*/10 * * * *'

# QA Agent - every 20 minutes (default)
schedule:
  - cron: '*/20 * * * *'
```

### Adjust Issue Count

Set repository variables:

```bash
gh variable set MIN_OPEN_ISSUES --body "5"
gh variable set MAX_ISSUES_TO_REVIEW --body "15"
```

### Customize Agent Behavior

Edit configuration in workflow files:

```yaml
env:
  ISSUE_LABELS_TO_HANDLE: 'feature,bug,documentation'
  ISSUE_LABELS_TO_SKIP: 'wontfix,duplicate,invalid'
  MAX_EXECUTION_TIME: '8'  # minutes
```

## Local Development

### Run Agents Locally

```bash
# Run issue resolver locally
cd .agents/scripts
./run_local.sh

# Debug agents
./debug_tools.sh

# Test agents
./test_agents.sh
```

### Local Environment Setup

```bash
# Copy example env file
cp src/claude-agent/.env.example src/claude-agent/.env

# Edit with your keys
vim src/claude-agent/.env
```

## Troubleshooting

### Agents Not Running

**Check:**
1. Workflows are enabled (Actions tab)
2. Secrets are set correctly
3. No workflow errors in Actions tab

**Fix:**
```bash
# Re-enable workflows
gh workflow enable issue-generator.yml
gh workflow enable issue-resolver.yml
gh workflow enable qa-agent.yml
```

### No Issues Being Created

**Check:**
1. Issue Generator workflow ran successfully
2. ANTHROPIC_API_KEY is valid
3. Check Actions logs for errors

**Fix:**
```bash
# Manually trigger
gh workflow run issue-generator.yml

# Check logs
gh run list --workflow=issue-generator.yml
```

### PRs Not Being Created

**Check:**
1. PAT_TOKEN has correct permissions
2. Token has `repo` and `workflow` scopes
3. Issue Resolver workflow succeeded

**Fix:**
```bash
# Regenerate PAT with correct scopes
# Then update secret
gh secret set PAT_TOKEN --body "new-token-here"
```

### See Full Troubleshooting Guide

[TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Security Best Practices

1. **Never commit `.env` files** - Already gitignored
2. **Rotate secrets every 90 days**
3. **Use GitHub Secrets** - Never hardcode
4. **Review PRs before merging** - Even AI-generated ones
5. **Monitor Actions logs** - Check for suspicious activity

See: [../SECURITY_AUDIT.md](../SECURITY_AUDIT.md)

## Next Steps

- ✅ Setup complete? → [USER_GUIDE.md](USER_GUIDE.md)
- 🤝 Want to contribute? → [../CONTRIBUTING_GUIDE.md](../CONTRIBUTING_GUIDE.md)
- 🔧 Need help? → [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- 📚 Learn more? → [INDEX.md](INDEX.md)

---

*Questions? Open an issue or check the [documentation index](INDEX.md)*
