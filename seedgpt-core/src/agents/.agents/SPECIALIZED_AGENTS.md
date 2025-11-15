# Specialized Issue Agents

## Overview

The specialized agent system provides domain-focused issue generation through a clean inheritance hierarchy. Each agent specializes in a specific business domain while sharing common functionality through the base class.

## Architecture

```
BaseIssueAgent (Abstract)
├── MarketingAgent
├── ProductAgent
└── SalesAgent
```

### Design Principles

1. **Single Responsibility**: Each agent focuses on one domain
2. **DRY (Don't Repeat Yourself)**: Common logic in base class
3. **Open/Closed**: Easy to extend with new agents
4. **Liskov Substitution**: All agents can be used interchangeably
5. **Dependency Inversion**: Agents depend on abstractions

## Base Class: `BaseIssueAgent`

Abstract base class providing:
- ✅ Issue generation workflow
- ✅ Deduplication checking
- ✅ Rate limiting
- ✅ Feedback loop integration
- ✅ Domain-specific issue filtering
- ✅ Claude AI integration (CLI or API)

### Required Implementations

Subclasses must implement:

```python
@abstractmethod
def get_agent_config(self) -> AgentConfig:
    """Return agent configuration"""
    pass

@abstractmethod
def build_domain_prompt(self, context: Dict) -> str:
    """Build domain-specific prompt additions"""
    pass
```

## Specialized Agents

### 1. MarketingAgent 🎯

**Domain**: Marketing and Growth

**Labels**: `marketing`, `growth`

**Focus Areas**:
- Content marketing and blog posts
- SEO optimization and analytics
- Social media campaigns
- Email marketing and newsletters
- Community building and engagement
- Brand awareness initiatives
- User acquisition strategies
- Marketing automation
- Landing pages and conversion optimization
- Partnership opportunities

**Use Cases**:
- Launch new marketing campaigns
- Improve SEO and content strategy
- Build community engagement
- Track marketing analytics
- Optimize conversion funnels

---

### 2. ProductAgent 🚀

**Domain**: Product Development

**Labels**: `product`, `feature`

**Focus Areas**:
- Feature development and enhancement
- User experience (UX) improvements
- User interface (UI) design
- Product analytics and metrics
- User research and feedback
- Product roadmap planning
- A/B testing and experiments
- Onboarding and user flows
- Accessibility improvements
- Mobile and responsive design

**Use Cases**:
- Plan new features
- Improve user experience
- Conduct user research
- Track product metrics
- Enhance accessibility

---

### 3. SalesAgent 💰

**Domain**: Sales and Revenue

**Labels**: `sales`, `revenue`

**Focus Areas**:
- Sales enablement and tools
- Pricing and monetization strategy
- Customer success and onboarding
- Sales funnel optimization
- CRM and sales automation
- Demo and trial experiences
- Customer support improvements
- Upsell and cross-sell opportunities
- Sales analytics and reporting
- Partnership and channel sales

**Use Cases**:
- Optimize sales funnel
- Improve pricing strategy
- Enhance customer success
- Build sales tools
- Increase revenue

## Usage

### Basic Usage

```python
from github import Github
from agents import MarketingAgent, ProductAgent, SalesAgent

# Initialize GitHub
g = Github(github_token)
repo = g.get_repo("owner/repo")

# Create specialized agents
marketing = MarketingAgent(repo, anthropic_api_key=api_key)
product = ProductAgent(repo, anthropic_api_key=api_key)
sales = SalesAgent(repo, anthropic_api_key=api_key)

# Generate issues for each domain
marketing.check_and_generate()
product.check_and_generate()
sales.check_and_generate()
```

### Custom Configuration

```python
from agents import MarketingAgent, AgentConfig

# Custom configuration
custom_config = AgentConfig(
    domain="marketing",
    default_labels=["marketing", "growth", "custom"],
    min_issues=5,
    focus_areas=["Custom focus area"],
    priority_keywords=["custom", "keywords"]
)

agent = MarketingAgent(
    repo=repo,
    anthropic_api_key=api_key,
    custom_config=custom_config
)
```

### Dry Mode (Testing)

```python
# Test without creating actual issues
agent = MarketingAgent(repo, anthropic_api_key=api_key, dry_mode=True)
agent.check_and_generate()  # Logs what would be created
```

## Creating New Specialized Agents

To create a new specialized agent:

1. **Create new file**: `src/agents/your_agent.py`

```python
from typing import Dict
from .base_issue_agent import BaseIssueAgent, AgentConfig

class YourAgent(BaseIssueAgent):
    """Your agent description"""
    
    def get_agent_config(self) -> AgentConfig:
        return AgentConfig(
            domain="your_domain",
            default_labels=["your", "labels"],
            min_issues=2,
            focus_areas=[
                "Focus area 1",
                "Focus area 2",
            ],
            priority_keywords=["keyword1", "keyword2"]
        )
    
    def build_domain_prompt(self, context: Dict) -> str:
        config = self.get_agent_config()
        
        prompt = f"""
🎯 YOUR DOMAIN FOCUS AREAS:
{chr(10).join([f"  • {area}" for area in config.focus_areas])}

Your task is to identify {context['needed']} opportunities.

Consider:
1. **Area 1**: What should we focus on?
2. **Area 2**: How can we improve?

Focus on actionable tasks that will:
- Achieve goal 1
- Achieve goal 2
"""
        return prompt
```

2. **Update `__init__.py`**:

```python
from .your_agent import YourAgent

__all__ = [..., "YourAgent"]
```

3. **Test your agent**:

```python
agent = YourAgent(repo, anthropic_api_key=api_key, dry_mode=True)
agent.check_and_generate()
```

## Features

### Domain-Specific Issue Filtering

Each agent only counts issues with its domain labels:

```python
# Marketing agent only counts issues with "marketing" or "growth" labels
marketing_issues = agent._filter_domain_issues(all_issues)
```

### Automatic Label Management

Agents automatically add domain labels to generated issues:

```python
# Even if Claude doesn't include labels, they're added automatically
issue['labels'] = list(set(issue['labels'] + self.config.default_labels))
```

### Rate Limiting

Each agent has independent rate limiting:
- Max 8 issues/hour
- Max 30 issues/day
- 10-minute cooldown between generations
- Quality and duplicate rate monitoring

### Deduplication

All agents use the same advanced deduplication:
- Title similarity (75% threshold)
- Body similarity (60% threshold)
- Semantic similarity (85% threshold)
- Quality gates (50% minimum score)

### Feedback Loop

Agents learn from historical data:
- Track success/failure rates
- Adapt prompts based on outcomes
- Prioritize high-performing issue types
- De-emphasize low-performing types

## Integration with GitHub Actions

### Example Workflow

```yaml
name: Specialized Issue Generation

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  generate-marketing-issues:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Marketing Agent
        run: python scripts/run_marketing_agent.py
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

  generate-product-issues:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Product Agent
        run: python scripts/run_product_agent.py
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

  generate-sales-issues:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Sales Agent
        run: python scripts/run_sales_agent.py
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Best Practices

1. **Use Dry Mode First**: Test with `dry_mode=True` before production
2. **Monitor Rate Limits**: Check logs for rate limit statistics
3. **Review Generated Issues**: Periodically review quality
4. **Adjust Configurations**: Tune `min_issues` based on needs
5. **Domain Separation**: Keep domains focused and non-overlapping
6. **Label Consistency**: Use consistent label naming across agents

## Troubleshooting

### No Issues Generated

- Check rate limits: `agent.rate_limiter.get_statistics()`
- Verify API keys are set
- Check if minimum issues already met
- Review logs for errors

### Duplicate Issues

- Deduplication is working correctly
- Adjust similarity thresholds if needed
- Review existing issues for clarity

### Wrong Domain Issues

- Verify label filtering logic
- Check `default_labels` configuration
- Ensure labels exist in repository

## Performance

- **Average generation time**: 10-30 seconds per agent
- **API calls**: 1 per generation (Claude)
- **GitHub API calls**: 2-3 (fetch issues, create issues)
- **Memory usage**: ~50MB per agent
- **Concurrent agents**: Safe to run in parallel

## Future Enhancements

- [ ] Multi-language support
- [ ] Custom prompt templates
- [ ] Integration with project management tools
- [ ] Advanced analytics dashboard
- [ ] Machine learning-based prioritization
- [ ] Cross-agent collaboration
- [ ] Issue dependency tracking
