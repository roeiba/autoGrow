# Quick Start: Specialized Agents

## 🚀 5-Minute Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export GITHUB_TOKEN="your_github_token"
export ANTHROPIC_API_KEY="your_anthropic_key"
export GITHUB_REPOSITORY="owner/repo"
```

### 3. Run Your First Agent

```bash
# Test in dry mode (no actual issues created)
python scripts/run_specialized_agents.py --agent marketing --dry-mode

# Run for real
python scripts/run_specialized_agents.py --agent marketing
```

## 📋 Common Use Cases

### Run All Agents

```bash
python scripts/run_specialized_agents.py
```

### Run Specific Agent

```bash
# Marketing
python scripts/run_specialized_agents.py --agent marketing

# Product
python scripts/run_specialized_agents.py --agent product

# Sales
python scripts/run_specialized_agents.py --agent sales
```

### Custom Configuration

```bash
# Maintain 5 issues per domain
python scripts/run_specialized_agents.py --min-issues 5

# Dry mode for testing
python scripts/run_specialized_agents.py --dry-mode
```

### Using Shell Scripts

```bash
# Marketing agent
./scripts/run_marketing_agent.sh

# Product agent
./scripts/run_product_agent.sh

# Sales agent
./scripts/run_sales_agent.sh
```

## 🐍 Python API

### Basic Usage

```python
from github import Github
from agents import MarketingAgent

# Initialize
g = Github("your_token")
repo = g.get_repo("owner/repo")

# Create agent
agent = MarketingAgent(
    repo=repo,
    anthropic_api_key="your_key"
)

# Generate issues
agent.check_and_generate()
```

### Advanced Usage

```python
from agents import ProductAgent, AgentConfig

# Custom configuration
config = AgentConfig(
    domain="product",
    default_labels=["product", "feature", "priority"],
    min_issues=5,
    focus_areas=["Custom area"],
    priority_keywords=["urgent", "critical"]
)

# Create agent with custom config
agent = ProductAgent(
    repo=repo,
    anthropic_api_key=api_key,
    custom_config=config,
    dry_mode=True  # Test mode
)

# Run
result = agent.check_and_generate()
```

## 🔧 GitHub Actions

### Manual Trigger

1. Go to **Actions** tab in GitHub
2. Select **Specialized Issue Agents**
3. Click **Run workflow**
4. Choose options:
   - Agent: marketing/product/sales/all
   - Dry mode: true/false
   - Min issues: 2-10

### Automated Schedule

The workflow runs automatically every 6 hours.

To change the schedule, edit `.github/workflows/specialized-agents.yml`:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
```

## 📊 What Each Agent Does

### 🎯 Marketing Agent

Creates issues for:
- Content marketing campaigns
- SEO optimization
- Social media strategies
- Email marketing
- Community engagement
- Growth tactics

**Labels**: `marketing`, `growth`

### 🚀 Product Agent

Creates issues for:
- New features
- UX improvements
- Product analytics
- User research
- A/B testing
- Accessibility

**Labels**: `product`, `feature`

### 💰 Sales Agent

Creates issues for:
- Sales enablement
- Pricing strategy
- Customer success
- Sales funnel optimization
- CRM improvements
- Revenue growth

**Labels**: `sales`, `revenue`

## 🎓 Examples

### Example 1: Weekly Marketing Sprint

```bash
# Generate 5 marketing issues for the week
python scripts/run_specialized_agents.py \
  --agent marketing \
  --min-issues 5
```

### Example 2: Product Roadmap Planning

```bash
# Generate product issues in dry mode first
python scripts/run_specialized_agents.py \
  --agent product \
  --min-issues 10 \
  --dry-mode

# Review the output, then run for real
python scripts/run_specialized_agents.py \
  --agent product \
  --min-issues 10
```

### Example 3: Sales Quarter Planning

```bash
# Generate sales initiatives
python scripts/run_specialized_agents.py \
  --agent sales \
  --min-issues 8
```

### Example 4: Full Business Review

```bash
# Run all agents with higher thresholds
python scripts/run_specialized_agents.py \
  --agent all \
  --min-issues 5
```

## 🔍 Monitoring

### Check Logs

```bash
# View detailed logs
tail -f logs/agents.log
```

### Rate Limit Status

The agents automatically track:
- Issues generated per hour/day
- Duplicate rate
- Quality rejection rate
- Cooldown status

Check logs for messages like:
```
[MARKETING] Rate limit stats: {...}
```

## 🐛 Troubleshooting

### "No issues generated"

✅ **Solution**: Minimum issues already met. Check current issues:

```bash
# Count marketing issues
gh issue list --label marketing

# Count product issues
gh issue list --label product

# Count sales issues
gh issue list --label sales
```

### "Rate limit exceeded"

✅ **Solution**: Wait for cooldown period (default: 60 minutes)

### "API key invalid"

✅ **Solution**: Verify environment variables:

```bash
echo $ANTHROPIC_API_KEY
echo $GITHUB_TOKEN
```

### "Import errors"

✅ **Solution**: Reinstall dependencies:

```bash
pip install -r requirements.txt --force-reinstall
```

## 📚 Next Steps

1. **Read Full Documentation**: `SPECIALIZED_AGENTS.md`
2. **Create Custom Agent**: Follow the guide in `SPECIALIZED_AGENTS.md`
3. **Integrate with CI/CD**: Use the GitHub Actions workflow
4. **Monitor Performance**: Review generated issues and adjust configs

## 💡 Pro Tips

1. **Start with Dry Mode**: Always test with `--dry-mode` first
2. **Adjust Min Issues**: Start low (2-3) and increase as needed
3. **Review Regularly**: Check generated issues weekly
4. **Use Labels**: Filter issues by agent labels for easy tracking
5. **Combine Agents**: Run all agents together for comprehensive coverage
6. **Monitor Quality**: Track duplicate and rejection rates in logs

## 🤝 Need Help?

- Check logs: `logs/agents.log`
- Review documentation: `SPECIALIZED_AGENTS.md`
- Open an issue: Use the bug report template
- Check examples: `scripts/run_specialized_agents.py`
