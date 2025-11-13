# Dry Mode for AI Agents

## Overview

Dry mode is a validation feature that allows AI agents to run without making actual changes to GitHub. This is useful for:

- **CI/CD Validation**: Test agent workflows in pull requests without side effects
- **Development Testing**: Validate agent logic without creating real issues or PRs
- **Debugging**: Trace agent execution flow without affecting production data

## How It Works

When dry mode is enabled (`DRY_MODE=true`), agents will:

1. ✅ Execute all read operations normally (fetch issues, read files, etc.)
2. ✅ Run AI analysis and generate fixes/issues
3. ✅ Create local git branches and commits
4. 🔍 **Skip** all GitHub write operations:
   - Creating/updating issues
   - Adding labels
   - Posting comments
   - Pushing branches
   - Creating pull requests

Instead of performing these operations, agents will log what they **would** do with a `🔍 DRY MODE:` prefix.

## Usage

### Environment Variable

Set the `DRY_MODE` environment variable to enable dry mode:

```bash
export DRY_MODE=true
```

Accepted values: `true`, `1`, `yes` (case-insensitive)

### Issue Resolver Agent

```python
from agents.issue_resolver import IssueResolver

agent = IssueResolver(
    repo=repo,
    git_repo=git_repo,
    anthropic_api_key=api_key,
    dry_mode=True  # Enable dry mode
)

agent.resolve_issue(specific_issue=123)
```

### Issue Generator Agent

```python
from agents.issue_generator import IssueGenerator

agent = IssueGenerator(
    repo=repo,
    anthropic_api_key=api_key,
    min_issues=3,
    dry_mode=True  # Enable dry mode
)

agent.check_and_generate()
```

### GitHub Actions

The `validate-agents.yml` workflow automatically runs agents in dry mode on every push and pull request:

```yaml
env:
  DRY_MODE: 'true'
```

## CI Validation Workflow

The `.github/workflows/validate-agents.yml` workflow validates:

1. **Issue Resolver Agent**: Can initialize and process issues without errors
2. **Issue Generator Agent**: Can generate issue suggestions without creating them
3. **Project Structure**: All required files and directories exist
4. **Python Syntax**: All agent code compiles without errors

This workflow runs on:
- Every push to `main` or `develop` branches
- Every pull request to `main`
- Manual trigger via `workflow_dispatch`

## Example Output

### Normal Mode
```
✅ Added 'in-progress' label
✅ Posted claim comment to issue
📤 Pushing branch 'fix/issue-123' to origin...
✅ Branch pushed successfully
🔀 Creating Pull Request...
✅ Pull Request created: #456
```

### Dry Mode
```
🔍 DRY MODE: Would add 'in-progress' label
🔍 DRY MODE: Would post claim comment to issue
🔍 DRY MODE: Would push branch 'fix/issue-123' to origin
🔍 DRY MODE: Would create pull request
🔍 DRY MODE: Would update issue with results
🎉 DRY MODE: WORKFLOW VALIDATION COMPLETED SUCCESSFULLY
```

## Benefits

1. **Safe Testing**: Test agent changes without affecting production
2. **Fast Feedback**: Validate workflows in CI without waiting for actual GitHub operations
3. **Cost Effective**: Reduce API calls and rate limit usage during development
4. **Debugging**: Trace execution flow without cleanup overhead

## Implementation Details

### Skipped Operations

When `dry_mode=True`, the following operations are skipped:

**Issue Resolver:**
- `issue.create_comment()` - Posting comments
- `issue.add_to_labels()` - Adding labels
- `origin.push()` - Pushing branches
- `repo.create_pull()` - Creating PRs

**Issue Generator:**
- `repo.create_issue()` - Creating issues

### Not Skipped

These operations still execute in dry mode:
- Reading repository data
- Fetching issues and PRs
- AI analysis and generation
- Local git operations (branch creation, commits)
- File system operations

## Related Files

- `src/agents/issue_resolver.py` - Core issue resolver with dry mode support
- `src/agents/issue_generator.py` - Core issue generator with dry mode support
- `.github/scripts/issue_resolver.py` - Wrapper script that reads `DRY_MODE` env var
- `.github/scripts/issue_generator.py` - Wrapper script that reads `DRY_MODE` env var
- `.github/workflows/validate-agents.yml` - CI validation workflow
