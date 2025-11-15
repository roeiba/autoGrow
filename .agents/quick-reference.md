# Quick Reference - Post-Refactoring

## Running Tests Locally

All commands must be run from the `seedgpt-core` directory:

```bash
# Navigate to seedgpt-core
cd seedgpt-core

# Run unit tests (fast, no API calls)
make test-unit

# Run CI flow (what GitHub Actions runs)
make ci-flow

# Run all tests including integration
make test-all

# Run with coverage
make test-coverage

# Clean temporary files
make clean
```

## Project Structure

```
ai-project-template/
├── .agents/                    # Agent configurations
├── .github/                    # CI/CD workflows ✅ UPDATED
│   ├── workflows/             # All workflows use seedgpt-core paths
│   └── scripts/               # Wrapper scripts
├── seedgpt-core/             # 🆕 Main codebase
│   ├── src/                   # Source code
│   ├── tests/                 # Test suite
│   ├── scripts/               # Utility scripts
│   └── Makefile*              # Build targets
├── PROJECT_BRIEF.md
├── README.md
└── CONTRIBUTING.md
```

## What Changed

### ✅ Updated Files
- All `.github/workflows/*.yml` files
- All paths now reference `seedgpt-core/`

### ⚠️ Important
- Run `make` commands from `seedgpt-core/` directory
- Update any local scripts to use new paths
- Update IDE configurations to point to `seedgpt-core/`

## GitHub Actions Status

After pushing, these workflows should pass:
- ✅ test-agents.yml (unit tests)
- ✅ validate-agents.yml (validation)
- ✅ sanity-tests.yml (sanity checks)
- ✅ issue-generator-agent.yml
- ✅ issue-resolver-agent.yml
- ✅ qa-agent.yml
- ✅ specialized-agents.yml

## Local Test Results

```
✅ 106 tests passed
⏭️  6 tests skipped
🔍 2 tests deselected
⏱️  Execution: 0.46s
```

## Next Steps

1. Commit changes:
   ```bash
   git add .github/workflows/ .agents/
   git commit -m "fix: update CI workflows for seedgpt-core structure"
   ```

2. Push to GitHub:
   ```bash
   git push origin main
   ```

3. Monitor GitHub Actions:
   - Go to repository → Actions tab
   - Verify all workflows pass

## Troubleshooting

### If tests fail locally:
```bash
cd seedgpt-core
make clean
make install-test-deps
make test-unit
```

### If GitHub Actions fail:
- Check workflow logs for specific errors
- Verify all paths use `seedgpt-core/` prefix
- Ensure requirements.txt is at `seedgpt-core/src/requirements.txt`

## Documentation

See `.agents/ci-workflow-migration.md` for full migration details.
