# Tests

This directory contains tests for the project.

## Structure

```
tests/
├── unit/                      # Unit tests
│   ├── test_gemini_agent.py  # GeminiAgent tests
│   └── __init__.py
├── integration/               # Integration tests (coming soon)
├── e2e/                      # End-to-end tests (coming soon)
├── fixtures/                 # Test fixtures and data (coming soon)
├── conftest.py               # Pytest configuration and fixtures
├── pytest.ini                # Pytest settings
├── requirements.txt          # Test dependencies
├── run_tests.sh             # Test runner script
└── README.md                # This file
```

## Current Test Coverage

### GeminiAgent Tests (`unit/test_gemini_agent.py`)
Comprehensive tests for the Gemini CLI Python wrapper:

- ✅ **Initialization** (7 tests)
  - API key handling (env var, explicit, missing)
  - Model and format configuration
  - Debug mode
  - Installation check

- ✅ **Installation Check** (3 tests)
  - Detection when installed
  - Detection when not found
  - Error handling

- ✅ **Query Method** (10 tests)
  - Basic queries
  - Include directories
  - YOLO mode
  - Custom models
  - Debug mode
  - Text vs JSON format
  - Error handling
  - API key in environment

- ✅ **Query with File** (3 tests)
  - File input handling
  - File not found errors
  - Custom model selection

- ✅ **Code Review** (1 test)
  - Review functionality and prompts

- ✅ **Generate Docs** (1 test)
  - Documentation generation

- ✅ **Analyze Logs** (2 tests)
  - Default and custom focus

- ✅ **Batch Process** (3 tests)
  - Success scenarios
  - Error handling
  - Custom file patterns

- ✅ **Integration Tests** (1 test)
  - Real API calls (requires API key)

**Total: 31 tests**

### ClaudeAgent Tests (`unit/test_claude_cli_agent.py`)
Comprehensive tests for the Claude Code CLI Python wrapper:

- ✅ **Initialization** (6 tests)
  - Default and custom parameters
  - Tool restrictions
  - Permission modes
  - Installation check

- ✅ **Installation Check** (3 tests)
  - Detection when installed
  - Detection when not found
  - Error handling

- ✅ **Command Building** (6 tests)
  - Basic command structure
  - Verbose mode
  - Tool restrictions
  - Permission modes
  - Additional arguments

- ✅ **Query Method** (6 tests)
  - Basic queries
  - System prompts
  - MCP configuration
  - Text vs JSON format
  - Error handling

- ✅ **Query with Stdin** (2 tests)
  - Stdin input handling
  - System prompt integration

- ✅ **Continue Conversation** (2 tests)
  - Continue most recent
  - Resume specific session

- ✅ **Code Review** (2 tests)
  - Review functionality
  - File not found errors

- ✅ **Generate Docs** (1 test)
  - Documentation generation

- ✅ **Fix Code** (1 test)
  - Code fixing functionality

- ✅ **Batch Process** (2 tests)
  - Success scenarios
  - Error handling

- ✅ **Integration Tests** (1 test)
  - Real CLI calls (requires installation)

**Total: 32 tests**

### Combined Test Coverage

**Unit Tests** (mocked, fast):
- **GeminiAgent**: 31 tests
- **ClaudeAgent**: 32 tests
- **Subtotal**: 63 tests

**Integration Tests** (real APIs, slow):
- **GeminiAgent**: 15 tests
- **ClaudeAgent**: 17 tests
- **Subtotal**: 32 tests

**Total**: 95 tests (63 unit + 32 integration)

## Running Tests

### Quick Start with Make (Recommended)
```bash
# Install dependencies
make install-test-deps

# Run unit tests only (fast, no API keys needed)
make test

# Run integration tests (requires API keys)
export GEMINI_API_KEY="your-key"
make test-integration

# Run all tests
make test-all

# Run with coverage
make test-coverage
```

### Manual Setup
```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run unit tests (excluding integration tests)
cd tests
./run_tests.sh

# Run with coverage
./run_tests.sh --coverage

# Run including integration tests (requires API keys)
./run_tests.sh --integration

# Run specific test file
./run_tests.sh unit/test_gemini_agent.py

# Run with verbose output
./run_tests.sh --verbose
```

### Python Tests (Manual)
```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_gemini_agent.py

# Run only unit tests (skip integration)
pytest -m "not integration"

# Run with verbose output
pytest -vv
```

### JavaScript/TypeScript Tests
```bash
# Install jest
npm install --save-dev jest

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## Writing Tests

### Python Example
```python
# tests/unit/test_example.py
import pytest
from src.module import function

def test_function():
    result = function(input)
    assert result == expected
```

### JavaScript Example
```javascript
// tests/unit/example.test.js
const { function } = require('../src/module');

test('function works correctly', () => {
  const result = function(input);
  expect(result).toBe(expected);
});
```

## Test Types

### Unit Tests (`unit/`)
- **Fast**: Run in < 1 second
- **Mocked**: No real API calls
- **Always run**: Part of CI/CD
- **No API keys needed**

### Integration Tests (`integration/`)
- **Slow**: Run in ~45 seconds
- **Real APIs**: Actual API calls
- **Run selectively**: Manual trigger in CI
- **API keys required**

## Best Practices

### Unit Tests
1. **Organize by type**: Unit, integration, and e2e tests in separate directories
2. **Name clearly**: Use descriptive test names that explain what is being tested
3. **One assertion per test**: Keep tests focused and simple
4. **Use fixtures**: Share test data and setup code
5. **Mock external dependencies**: Isolate the code under test
6. **Test edge cases**: Include boundary conditions and error cases
7. **Keep tests fast**: Unit tests should run quickly

### Integration Tests
1. **Mark with `@pytest.mark.integration`**
2. **Mark slow tests with `@pytest.mark.slow`**
3. **Handle API errors gracefully**
4. **Use temporary files**
5. **Document API costs**
6. **Skip if API keys not set**

## Documentation

- **Unit Tests**: This file (README.md)
- **Integration Tests**: See [INTEGRATION_TESTS.md](INTEGRATION_TESTS.md)
- **Testing Guide**: See [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Makefile Guide**: See [../MAKEFILE_GUIDE.md](../MAKEFILE_GUIDE.md)

## CI/CD Integration

Tests are automatically run in CI/CD pipelines. See `.github/workflows/test-agents.yml` for configuration.

**GitHub Actions Workflow**:
- Runs unit tests on push/PR
- Runs on multiple OS (Ubuntu, macOS)
- Runs on multiple Python versions (3.9, 3.10, 3.11)
- Integration tests via manual trigger
- Coverage reports uploaded to Codecov
