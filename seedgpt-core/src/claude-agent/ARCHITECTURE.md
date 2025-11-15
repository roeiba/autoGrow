# Claude Agent Architecture

## Overview

The Claude Agent is a professional, production-ready autonomous system that uses Claude AI to automatically resolve GitHub issues and create pull requests.

## Design Principles

1. **Separation of Concerns**: Shell scripts only for Docker entrypoint, Python for all business logic
2. **Configuration Management**: Centralized config with environment variable validation
3. **Structured Logging**: Professional logging with timestamps and levels
4. **Error Handling**: Comprehensive exception handling with proper error propagation
5. **Testability**: Modular design with unit tests
6. **Maintainability**: Clean code structure with type hints and docstrings

## Project Structure

```
claude-agent/
├── Dockerfile                  # Container definition (Python 3.11-slim base)
├── docker-compose.yml          # Orchestration configuration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore patterns
├── run-agent.sh               # Convenience runner script
├── README.md                  # User documentation
├── ARCHITECTURE.md            # This file
│
├── src/                       # Python source code
│   ├── __init__.py
│   ├── agentic_workflow.py    # Main workflow orchestrator
│   ├── config.py              # Configuration management
│   └── utils/
│       ├── __init__.py
│       └── logger.py          # Logging configuration
│
├── tests/                     # Test suite
│   ├── __init__.py
│   └── test_agentic_workflow.py
│
├── scripts/                   # Shell scripts (minimal)
│   └── entrypoint.sh          # Docker entrypoint only
│
└── .agents/                   # Agent metadata
    └── refactor_script.sh     # Development utilities
```

## Component Architecture

### 1. Entry Point (`scripts/entrypoint.sh`)

**Purpose**: Minimal shell script for Docker container initialization

**Responsibilities**:
- Validate environment variables
- Authenticate with GitHub CLI
- Execute Python workflow
- Handle exit codes

**Why Shell**: Required for Docker ENTRYPOINT, keeps it minimal

### 2. Configuration (`src/config.py`)

**Purpose**: Centralized configuration management

**Features**:
- `AgentConfig` dataclass for type-safe configuration
- Environment variable loading with `from_env()`
- Validation of required fields
- Helper properties (e.g., `is_dry_run`)

**Benefits**:
- Single source of truth for configuration
- Easy to test with mock configs
- Type hints for IDE support

### 3. Logging (`src/utils/logger.py`)

**Purpose**: Structured logging system

**Features**:
- Timestamp formatting
- Log level support (INFO, ERROR, etc.)
- Console output with colors
- Consistent format across application

**Example Output**:
```
[2024-11-13 10:30:45] INFO: Agent workflow initialized
[2024-11-13 10:30:46] INFO: Cloning repository: owner/repo
[2024-11-13 10:30:50] ERROR: Error fetching issue: Not Found
```

### 4. Main Workflow (`src/agentic_workflow.py`)

**Purpose**: Core business logic for issue resolution

**Class**: `AgenticWorkflow`

**Key Methods**:

| Method | Purpose |
|--------|---------|
| `__init__()` | Initialize with config, logger, and API clients |
| `_parse_repo_info()` | Extract owner/repo from URL |
| `_clone_repository()` | Clone target repository with authentication |
| `_get_issue()` | Fetch issue details from GitHub API |
| `_create_branch()` | Create fix branch with timestamp |
| `_analyze_codebase()` | Detect languages and frameworks |
| `_generate_fix_with_claude()` | Use Claude AI to generate fix |
| `_apply_fix()` | Apply Claude's suggested changes |
| `_commit_and_push()` | Commit changes and push to GitHub |
| `_create_pull_request()` | Create PR with detailed description |
| `run()` | Execute complete workflow |

**Workflow Sequence**:

```
1. Initialize (config, logger, API clients)
2. Parse repository information
3. Clone repository
4. Get issue details (auto-select or specified)
5. Create fix branch
6. Analyze codebase structure
7. Generate fix with Claude AI
8. Apply fix to files
9. Commit and push changes
10. Create pull request
11. Return success/failure
```

## Data Flow

```
Environment Variables
        ↓
    AgentConfig
        ↓
  AgenticWorkflow
        ↓
    ┌───────────────┐
    │  GitHub API   │ ← Fetch issue
    └───────────────┘
        ↓
    ┌───────────────┐
    │  Claude API   │ ← Generate fix
    └───────────────┘
        ↓
    File System ← Apply changes
        ↓
    ┌───────────────┐
    │  Git/GitHub   │ ← Push & create PR
    └───────────────┘
```

## API Integration

### GitHub API (PyGithub)

**Used For**:
- Fetching issue details
- Creating pull requests
- Repository operations

**Authentication**: Personal Access Token via `Github(token)`

### Anthropic API

**Used For**:
- Analyzing issues
- Generating code fixes
- Providing implementation guidance

**Model**: `claude-3-5-sonnet-20241022`

**Authentication**: API key via `Anthropic(api_key)`

### Git Operations (GitPython)

**Used For**:
- Cloning repositories
- Creating branches
- Committing changes
- Pushing to remote

**Authentication**: Token embedded in remote URL

## Error Handling Strategy

### Levels of Error Handling

1. **Validation Errors**: Caught at config initialization
   - Missing environment variables
   - Invalid repository URLs

2. **API Errors**: Caught and logged with context
   - GitHub API failures (network, auth, not found)
   - Claude API failures (rate limits, invalid requests)

3. **Git Errors**: Caught during repository operations
   - Clone failures
   - Push failures
   - Merge conflicts

4. **Workflow Errors**: Caught at top level in `run()`
   - Logged with full traceback
   - Return non-zero exit code

### Error Propagation

```python
try:
    # Operation
except SpecificException as e:
    self.logger.error(f"Context: {e}")
    raise  # Propagate to caller
```

## Testing Strategy

### Unit Tests (`tests/test_agentic_workflow.py`)

**Coverage**:
- Configuration validation
- Repository URL parsing
- Codebase analysis
- Mock API interactions

**Tools**:
- pytest for test framework
- pytest-mock for mocking
- pytest-cov for coverage

**Run Tests**:
```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html
```

### Integration Testing

**Manual Testing**:
1. Test with real repository
2. Verify issue fetching
3. Check Claude API integration
4. Validate PR creation

**Dry Run Mode**:
```bash
AGENT_MODE=dry-run docker-compose up
```

## Security Considerations

### Secrets Management

1. **Environment Variables**: Never commit `.env` files
2. **Token Scoping**: Use minimal required GitHub permissions
3. **API Keys**: Rotate regularly, monitor usage
4. **Git History**: Tokens embedded in URLs not logged

### Container Security

1. **Base Image**: Official Python slim image
2. **User**: Runs as root (consider non-root user)
3. **Network**: No exposed ports
4. **Volumes**: Workspace isolated

### Code Security

1. **Input Validation**: All URLs and inputs validated
2. **Path Traversal**: Paths resolved within workspace
3. **Command Injection**: No shell command construction from user input
4. **Dependency Scanning**: Regular updates of requirements.txt

## Performance Considerations

### Optimization Points

1. **Repository Cloning**: Shallow clone for large repos
2. **API Calls**: Batch requests where possible
3. **File Operations**: Stream large files
4. **Memory**: Limit Claude response size

### Resource Limits

```yaml
# docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
```

## Extensibility

### Adding New Features

1. **New AI Providers**: Create provider interface
2. **Custom Workflows**: Extend `AgenticWorkflow` class
3. **Additional Checks**: Add methods to workflow
4. **Notification Systems**: Add notification module

### Configuration Extensions

```python
@dataclass
class AgentConfig:
    # ... existing fields ...
    slack_webhook: Optional[str] = None
    max_retries: int = 3
    timeout_seconds: int = 300
```

## Deployment Patterns

### Single Run

```bash
docker-compose up
```

### Scheduled Execution

```bash
# Cron job
0 2 * * * cd /path/to/claude-agent && ./run-agent.sh
```

### CI/CD Integration

```yaml
# GitHub Actions
- name: Run Claude Agent
  run: docker-compose up
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Kubernetes Deployment

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: claude-agent
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: claude-agent
            image: claude-agent:latest
            envFrom:
            - secretRef:
                name: claude-agent-secrets
```

## Monitoring and Observability

### Logging

- Structured logs to stdout
- Timestamp on every log line
- Log levels for filtering
- Contextual information

### Metrics (Future)

- Issues processed
- Success/failure rate
- API call latency
- PR merge rate

### Alerting (Future)

- Failed runs
- API errors
- Rate limit warnings

## Future Enhancements

1. **Multi-Issue Processing**: Handle multiple issues in one run
2. **Testing Integration**: Run tests before creating PR
3. **Code Review**: Self-review before submission
4. **Learning System**: Improve based on PR feedback
5. **Webhook Integration**: Trigger on issue creation
6. **Dashboard**: Web UI for monitoring
7. **Analytics**: Track performance metrics

## Development Workflow

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run locally (without Docker)
export GITHUB_TOKEN=...
export ANTHROPIC_API_KEY=...
export REPO_URL=...
python src/agentic_workflow.py
```

### Building Docker Image

```bash
docker-compose build
```

### Debugging

```bash
# Interactive shell in container
docker run -it --entrypoint /bin/bash claude-agent

# View logs
docker-compose logs -f
```

## Contributing Guidelines

1. **Code Style**: Follow PEP 8
2. **Type Hints**: Add to all functions
3. **Docstrings**: Document all public methods
4. **Tests**: Add tests for new features
5. **Logging**: Use logger, not print
6. **Error Handling**: Catch and log appropriately

## License

Part of the AI Project Template. See main repository for license details.
