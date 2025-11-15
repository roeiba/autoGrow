# Agents Module - Architecture Documentation

## Overview

The `src/agents/` module contains the **core business logic** for all GitHub automation agents. This follows the principle of **separation of concerns** where:

- **Core Logic** (`src/agents/`) - Reusable, testable agent implementations
- **CI/CD Wrappers** (`.github/scripts/`) - Thin wrapper scripts for GitHub Actions workflows

## Architecture

```
src/agents/
├── __init__.py              # Package exports
├── issue_generator.py       # Core: Issue generation logic
├── issue_resolver.py        # Core: Issue resolution logic
├── qa_agent.py             # Core: QA monitoring logic
├── base_issue_agent.py     # Core: Base class for specialized agents
├── marketing_agent.py      # Core: Marketing-focused issue generation
├── product_agent.py        # Core: Product-focused issue generation
├── sales_agent.py          # Core: Sales-focused issue generation
└── .agents/
    ├── README.md           # This file
    ├── SPECIALIZED_AGENTS.md  # Specialized agents documentation
    ├── QUICK_START.md      # Quick start guide
    └── ARCHITECTURE.md     # Architecture diagrams

.github/scripts/
├── issue_generator.py      # Wrapper: Env setup + calls core module
├── issue_resolver.py       # Wrapper: Env setup + calls core module
└── qa_agent.py            # Wrapper: Env setup + calls core module
```

## Design Principles

### 1. **Core Logic in `src/agents/`**

All agent implementations are classes with clear responsibilities:

**General Agents:**
- **`IssueGenerator`** - Generates GitHub issues using AI
- **`IssueResolver`** - Resolves issues and creates PRs
- **`QAAgent`** - Monitors repository health

**Specialized Issue Agents:**
- **`BaseIssueAgent`** - Abstract base class for domain-specific agents
- **`MarketingAgent`** - Generates marketing and growth-related issues
- **`ProductAgent`** - Generates product and feature-related issues
- **`SalesAgent`** - Generates sales and revenue-related issues

These classes are:
- ✅ **Testable** - Can be unit tested independently
- ✅ **Reusable** - Can be imported and used in other contexts
- ✅ **Maintainable** - Single source of truth for logic
- ✅ **Configurable** - Accept parameters for flexibility

### 2. **Thin Wrappers in `.github/scripts/`**

GitHub Actions workflow scripts are minimal wrappers that:

1. Read environment variables
2. Initialize GitHub/Git clients
3. Instantiate core agent classes
4. Call agent methods
5. Handle errors

**Example:**

```python
# .github/scripts/issue_generator.py
from agents.issue_generator import IssueGenerator

# Setup from environment
repo = gh.get_repo(REPO_NAME)

# Use core logic
agent = IssueGenerator(repo=repo, min_issues=MIN_ISSUES)
agent.check_and_generate()
```

### 3. **Benefits of This Architecture**

| Aspect | Before | After |
|--------|--------|-------|
| **Testing** | Hard to test CI scripts | Easy to unit test core classes |
| **Reusability** | Logic locked in CI scripts | Can use agents anywhere |
| **Maintenance** | Duplicate code in scripts | Single source of truth |
| **Development** | Must test via CI | Can test locally |
| **Integration** | Tight coupling to GitHub Actions | Loose coupling via interfaces |

## Usage Examples

### Using Core Agents Directly

```python
from github import Github, Auth
from agents.issue_generator import IssueGenerator

# Initialize
auth = Auth.Token(token)
gh = Github(auth=auth)
repo = gh.get_repo("owner/repo")

# Use agent
generator = IssueGenerator(
    repo=repo,
    anthropic_api_key="sk-...",
    min_issues=5
)

# Run
generator.check_and_generate()
```

### Testing Core Agents

```python
import pytest
from unittest.mock import Mock
from agents.issue_generator import IssueGenerator

def test_issue_generator():
    # Mock GitHub repo
    mock_repo = Mock()
    mock_repo.get_issues.return_value = []
    
    # Test agent
    agent = IssueGenerator(repo=mock_repo, min_issues=3)
    result = agent.check_and_generate()
    
    assert result == True
```

## Migration Notes

### What Changed

1. **Moved** core logic from `.github/scripts/*.py` to `src/agents/*.py`
2. **Refactored** monolithic scripts into reusable classes
3. **Created** thin wrapper scripts in `.github/scripts/`
4. **Maintained** backward compatibility with existing workflows

### What Stayed the Same

- ✅ GitHub Actions workflows unchanged
- ✅ Environment variables unchanged
- ✅ Workflow triggers unchanged
- ✅ Functionality unchanged

### Breaking Changes

**None** - This is a pure refactoring with no breaking changes.

## Development Workflow

### Local Development

```bash
# Test agents locally
cd src/agents
python -m pytest tests/

# Run agent directly
python -c "
from agents.issue_generator import IssueGenerator
# ... setup and run
"
```

### CI/CD

Workflows continue to work as before:

```yaml
# .github/workflows/issue-generator-agent.yml
- name: Run generator
  run: python .github/scripts/issue_generator.py
```

The wrapper script handles environment setup and calls the core module.

## Future Enhancements

### Potential Improvements

1. **Add comprehensive unit tests** for each agent class
2. **Create integration tests** that mock GitHub API
3. **Add CLI interface** for running agents from command line
4. **Create agent base class** for shared functionality
5. **Add configuration files** instead of environment variables
6. **Implement agent orchestration** for complex workflows

### Example: CLI Interface

```bash
# Future enhancement
python -m agents.issue_generator \
  --repo owner/repo \
  --min-issues 5 \
  --api-key sk-...
```

## Dependencies

Core agents depend on:

- `PyGithub` - GitHub API client
- `GitPython` - Git operations (for IssueResolver)
- `anthropic` or `claude_cli_agent` - AI functionality
- `src/utils/project_brief_validator.py` - Validation utilities

## Related Documentation

- [Specialized Agents Guide](./SPECIALIZED_AGENTS.md) - Complete guide to specialized agents
- [Quick Start Guide](./QUICK_START.md) - Get started with specialized agents
- [Architecture Diagrams](./ARCHITECTURE.md) - Visual architecture documentation
- [GitHub Workflows](../../../.github/workflows/README.md)
- [Project Brief Validator](../../utils/project_brief_validator.py)
- [Claude Agent SDK](../../claude-agent/README.md)

## Maintenance

### Adding a New Agent

1. Create `src/agents/new_agent.py` with core logic
2. Create `.github/scripts/new_agent.py` wrapper
3. Add workflow in `.github/workflows/new-agent.yml`
4. Update `src/agents/__init__.py` exports
5. Add tests in `tests/unit/test_new_agent.py`

### Modifying an Existing Agent

1. Update core logic in `src/agents/*.py`
2. Wrapper scripts usually don't need changes
3. Update tests if behavior changed
4. Document changes in CHANGELOG.md

---

**Last Updated:** November 2025  
**Refactoring:** Core agent logic separation from CI/CD layer
