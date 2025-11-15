# Agent Architecture Refactoring

## Summary

Refactored core agent logic from `.github/scripts/` to `src/agents/` to follow proper separation of concerns and improve maintainability.

## What Changed

### Before

```
.github/scripts/
├── issue_generator.py    (225 lines - monolithic script)
├── issue_resolver.py     (398 lines - monolithic script)
└── qa_agent.py          (404 lines - monolithic script)
```

**Problems:**
- ❌ Core logic mixed with CI/CD concerns
- ❌ Hard to test independently
- ❌ Not reusable outside GitHub Actions
- ❌ Difficult to maintain and extend

### After

```
src/agents/
├── __init__.py              (Package exports)
├── issue_generator.py       (Core logic - 250 lines)
├── issue_resolver.py        (Core logic - 350 lines)
├── qa_agent.py             (Core logic - 380 lines)
└── .agents/README.md       (Architecture docs)

.github/scripts/
├── issue_generator.py      (Thin wrapper - 52 lines)
├── issue_resolver.py       (Thin wrapper - 61 lines)
└── qa_agent.py            (Thin wrapper - 59 lines)
```

**Benefits:**
- ✅ Clear separation of concerns
- ✅ Core logic is testable and reusable
- ✅ Thin CI/CD wrappers (< 100 lines each)
- ✅ Easy to maintain and extend
- ✅ Can use agents outside GitHub Actions

## Architecture

### Core Agents (`src/agents/`)

**IssueGenerator**
```python
class IssueGenerator:
    def __init__(self, repo, anthropic_api_key, min_issues):
        ...
    
    def check_and_generate(self) -> bool:
        """Check issue count and generate if needed"""
```

**IssueResolver**
```python
class IssueResolver:
    def __init__(self, repo, git_repo, anthropic_api_key, labels_to_handle, ...):
        ...
    
    def resolve_issue(self, specific_issue=None) -> bool:
        """Resolve an issue and create a PR"""
```

**QAAgent**
```python
class QAAgent:
    def __init__(self, repo, anthropic_api_key, max_issues_to_review, ...):
        ...
    
    def run_qa_check(self) -> bool:
        """Run QA check on repository"""
```

### CI/CD Wrappers (`.github/scripts/`)

Each wrapper:
1. Reads environment variables
2. Initializes GitHub/Git clients
3. Instantiates core agent class
4. Calls agent method
5. Handles errors

**Example:**
```python
# .github/scripts/issue_generator.py
from agents.issue_generator import IssueGenerator

# Setup
repo = gh.get_repo(REPO_NAME)

# Run
agent = IssueGenerator(repo=repo, min_issues=MIN_ISSUES)
agent.check_and_generate()
```

## Migration Impact

### No Breaking Changes

- ✅ GitHub Actions workflows unchanged
- ✅ Environment variables unchanged
- ✅ Workflow behavior unchanged
- ✅ All functionality preserved

### What's Better

| Aspect | Improvement |
|--------|-------------|
| **Testability** | Can now unit test core logic independently |
| **Reusability** | Agents can be used in other contexts (CLI, API, etc.) |
| **Maintainability** | Single source of truth for each agent |
| **Development** | Can test locally without CI |
| **Code Quality** | Clear separation of concerns |

## Usage Examples

### In GitHub Actions (Unchanged)

```yaml
# .github/workflows/issue-generator-agent.yml
- name: Run generator
  run: python .github/scripts/issue_generator.py
```

### Direct Usage (New Capability)

```python
from github import Github, Auth
from agents.issue_generator import IssueGenerator

auth = Auth.Token(token)
gh = Github(auth=auth)
repo = gh.get_repo("owner/repo")

agent = IssueGenerator(repo=repo, min_issues=5)
agent.check_and_generate()
```

### Testing (New Capability)

```python
import pytest
from unittest.mock import Mock
from agents.issue_generator import IssueGenerator

def test_issue_generator():
    mock_repo = Mock()
    mock_repo.get_issues.return_value = []
    
    agent = IssueGenerator(repo=mock_repo, min_issues=3)
    result = agent.check_and_generate()
    
    assert result == True
```

## File Structure

```
ai-project-template/
├── .github/
│   ├── scripts/
│   │   ├── issue_generator.py    ← Thin wrapper (52 lines)
│   │   ├── issue_resolver.py     ← Thin wrapper (61 lines)
│   │   └── qa_agent.py           ← Thin wrapper (59 lines)
│   └── workflows/
│       ├── issue-generator-agent.yml   ← Renamed
│       ├── issue-resolver-agent.yml    ← Renamed
│       └── qa-agent.yml          ← Unchanged
│
├── src/
│   ├── agents/                   ← NEW: Core agent logic
│   │   ├── __init__.py
│   │   ├── issue_generator.py    ← Core logic (250 lines)
│   │   ├── issue_resolver.py     ← Core logic (350 lines)
│   │   ├── qa_agent.py           ← Core logic (380 lines)
│   │   └── .agents/
│   │       └── README.md         ← Architecture docs
│   │
│   └── utils/
│       └── project_brief_validator.py  ← Used by agents
│
└── tests/
    ├── unit/
    │   ├── test_issue_generator.py     ← Can add tests
    │   ├── test_issue_resolver.py      ← Can add tests
    │   └── test_qa_agent.py            ← Can add tests
    └── integration/
        └── test_agents_integration.py  ← Can add tests
```

## Next Steps

### Recommended Enhancements

1. **Add Unit Tests**
   ```bash
   tests/unit/test_issue_generator.py
   tests/unit/test_issue_resolver.py
   tests/unit/test_qa_agent.py
   ```

2. **Add Integration Tests**
   ```bash
   tests/integration/test_agents_integration.py
   ```

3. **Create CLI Interface**
   ```bash
   python -m agents.issue_generator --repo owner/repo --min-issues 5
   ```

4. **Add Agent Base Class**
   ```python
   class BaseAgent:
       """Base class for all agents"""
       def __init__(self, repo, anthropic_api_key):
           self.repo = repo
           self.anthropic_api_key = anthropic_api_key
   ```

5. **Configuration Files**
   ```yaml
   # agents.yml
   issue_generator:
     min_issues: 5
     labels: [feature, bug, documentation]
   ```

## Documentation

- **Architecture Details:** `src/agents/.agents/README.md`
- **Workflow Documentation:** `.github/workflows/README.md`
- **Testing Guide:** `tests/README.md`

## Maintenance

### Modifying an Agent

1. Update core logic in `src/agents/*.py`
2. Wrapper scripts usually don't need changes
3. Update tests if behavior changed
4. Document in CHANGELOG.md

### Adding a New Agent

1. Create `src/agents/new_agent.py` with core logic
2. Create `.github/scripts/new_agent.py` wrapper
3. Add workflow in `.github/workflows/new-agent.yml`
4. Update `src/agents/__init__.py` exports
5. Add tests

---

**Refactoring Date:** November 2025  
**Impact:** Zero breaking changes, improved architecture  
**Status:** ✅ Complete
