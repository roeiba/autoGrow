#!/bin/bash

# Run tests for the project
# Usage: ./run_tests.sh [options]

set -e

cd "$(dirname "$0")"

echo "🧪 Running Tests"
echo "=" * 50

# Check if pytest is installed
if ! python3 -c "import pytest" 2>/dev/null; then
    echo "⚠️  pytest not found. Installing test dependencies..."
    pip3 install -r requirements.txt
fi

# Parse arguments
RUN_INTEGRATION=false
RUN_COVERAGE=false
VERBOSE=false
TEST_PATH=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --integration|-i)
            RUN_INTEGRATION=true
            shift
            ;;
        --coverage|-c)
            RUN_COVERAGE=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        *)
            TEST_PATH="$1"
            shift
            ;;
    esac
done

# Build pytest command
PYTEST_CMD="pytest"

if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -vv"
fi

if [ "$RUN_COVERAGE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=../src --cov-report=html --cov-report=term"
fi

if [ "$RUN_INTEGRATION" = false ]; then
    PYTEST_CMD="$PYTEST_CMD -m 'not integration'"
fi

if [ -n "$TEST_PATH" ]; then
    PYTEST_CMD="$PYTEST_CMD $TEST_PATH"
fi

echo ""
echo "Running: $PYTEST_CMD"
echo ""

# Run tests
eval $PYTEST_CMD

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    
    if [ "$RUN_COVERAGE" = true ]; then
        echo ""
        echo "📊 Coverage report generated in htmlcov/index.html"
    fi
else
    echo ""
    echo "❌ Some tests failed (exit code: $EXIT_CODE)"
fi

exit $EXIT_CODE
