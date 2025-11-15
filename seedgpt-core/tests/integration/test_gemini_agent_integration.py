#!/usr/bin/env python3
"""
Integration tests for GeminiAgent - REAL API calls
These tests require actual Gemini API key and gemini-cli installation
"""

import pytest
import os
import sys
import json
import tempfile
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "gemini-agent"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from gemini_agent import GeminiAgent
from utils.exceptions import (
    ConfigurationError,
    FileOperationError,
)


@pytest.fixture
def api_key():
    """Get API key from environment"""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        pytest.skip("GEMINI_API_KEY not set - skipping integration tests")
    return key


@pytest.fixture
def agent(api_key):
    """Create a real GeminiAgent instance"""
    return GeminiAgent(api_key=api_key, output_format="json")


@pytest.fixture
def temp_python_file(tmp_path):
    """Create a temporary Python file for testing"""
    file_path = tmp_path / "test_code.py"
    file_path.write_text(
        """
def add(a, b):
    '''Add two numbers'''
    return a + b

def multiply(a, b):
    '''Multiply two numbers'''
    return a * b

if __name__ == '__main__':
    print(add(2, 3))
    print(multiply(4, 5))
"""
    )
    return str(file_path)


@pytest.fixture
def temp_buggy_file(tmp_path):
    """Create a temporary file with a bug"""
    file_path = tmp_path / "buggy_code.py"
    file_path.write_text(
        """
def divide(a, b):
    '''Divide two numbers'''
    return a / b  # Bug: no zero division check

def process_list(items):
    '''Process a list of items'''
    return items[0]  # Bug: no empty list check
"""
    )
    return str(file_path)


class TestGeminiAgentIntegrationBasic:
    """Basic integration tests"""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_real_query(self, agent):
        """Test real query to Gemini API"""
        result = agent.query("Say 'integration test successful' and nothing else")

        assert result is not None
        assert "response" in result or "text" in result or "result" in result

        # Extract response text
        response_text = (
            result.get("response")
            or result.get("text")
            or result.get("result")
            or str(result)
        ).lower()

        assert "integration" in response_text or "successful" in response_text

    @pytest.mark.integration
    @pytest.mark.slow
    def test_real_query_with_model(self, agent):
        """Test query with specific model"""
        result = agent.query(
            "What is 2+2? Answer with just the number.", model="gemini-pro"
        )

        assert result is not None
        response_text = str(result).lower()
        assert "4" in response_text


class TestGeminiAgentIntegrationFiles:
    """Integration tests with file operations"""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_real_query_with_file(self, agent, temp_python_file):
        """Test query with real file input"""
        result = agent.query_with_file(
            "List the functions in this Python file", temp_python_file
        )

        assert result is not None
        response_text = str(result).lower()
        assert "add" in response_text or "multiply" in response_text

    @pytest.mark.integration
    @pytest.mark.slow
    def test_real_code_review(self, agent, temp_python_file):
        """Test real code review"""
        result = agent.code_review(temp_python_file)

        assert result is not None
        response_text = str(result).lower()
        # Should mention code quality or review
        assert any(
            word in response_text
            for word in ["code", "function", "review", "quality", "good", "clean"]
        )

    @pytest.mark.integration
    @pytest.mark.slow
    def test_real_generate_docs(self, agent, temp_python_file):
        """Test real documentation generation"""
        result = agent.generate_docs(temp_python_file)

        assert result is not None
        response_text = str(result).lower()
        # Should mention documentation or functions
        assert any(
            word in response_text
            for word in ["add", "multiply", "function", "parameter", "return"]
        )

    @pytest.mark.integration
    @pytest.mark.slow
    def test_real_analyze_logs(self, agent, tmp_path):
        """Test real log analysis"""
        log_file = tmp_path / "test.log"
        log_file.write_text(
            """
2025-11-13 10:00:00 INFO Application started
2025-11-13 10:00:01 ERROR Connection failed: timeout
2025-11-13 10:00:02 ERROR Database error: connection refused
2025-11-13 10:00:03 INFO Retrying connection
2025-11-13 10:00:04 INFO Connection successful
"""
        )

        result = agent.analyze_logs(str(log_file))

        assert result is not None
        response_text = str(result).lower()
        # Should mention errors or issues
        assert any(
            word in response_text
            for word in ["error", "connection", "timeout", "issue", "problem"]
        )


class TestGeminiAgentIntegrationBatch:
    """Integration tests for batch processing"""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_real_batch_process(self, agent, tmp_path):
        """Test real batch processing"""
        # Create multiple test files
        for i in range(3):
            file_path = tmp_path / f"file{i}.py"
            file_path.write_text(
                f"""
def function_{i}():
    '''Function number {i}'''
    return {i}
"""
            )

        results = agent.batch_process(
            str(tmp_path), "List the function name in this file", file_pattern="*.py"
        )

        assert len(results) == 3
        assert all(r["success"] for r in results)

        # Check that each result mentions the function
        for i, result in enumerate(results):
            response_text = str(result["result"]).lower()
            assert f"function_{i}" in response_text or f"function {i}" in response_text


class TestGeminiAgentIntegrationOptions:
    """Integration tests for various options"""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_real_query_with_yolo(self, agent):
        """Test query with yolo mode"""
        result = agent.query("Say 'yolo mode works'", yolo=True)

        assert result is not None

    @pytest.mark.integration
    @pytest.mark.slow
    def test_real_query_with_debug(self, api_key):
        """Test query with debug mode"""
        debug_agent = GeminiAgent(api_key=api_key, debug=True)
        result = debug_agent.query("Say 'debug mode works'")

        assert result is not None

    @pytest.mark.integration
    @pytest.mark.slow
    def test_real_query_json_format(self, api_key):
        """Test query with JSON output format"""
        json_agent = GeminiAgent(api_key=api_key, output_format="json")
        result = json_agent.query("What is Python?")

        assert result is not None
        # Should be parseable as JSON or dict
        assert isinstance(result, (dict, str))


class TestGeminiAgentIntegrationErrorHandling:
    """Integration tests for error handling"""

    @pytest.mark.integration
    def test_invalid_api_key(self):
        """Test with invalid API key (gemini-cli not installed)"""
        with pytest.raises(ConfigurationError):
            agent = GeminiAgent(api_key="invalid_key_12345")
            agent.query("test")

    @pytest.mark.integration
    def test_file_not_found(self, agent):
        """Test with non-existent file"""
        with pytest.raises(FileOperationError):
            agent.query_with_file("test", "/nonexistent/file.py")

    @pytest.mark.integration
    def test_empty_prompt(self, agent):
        """Test with empty prompt"""
        with pytest.raises((ValueError, RuntimeError)):
            agent.query("")


class TestGeminiAgentIntegrationEndToEnd:
    """End-to-end integration tests"""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_complete_workflow(self, agent, temp_buggy_file):
        """Test complete workflow: review -> identify issues -> suggest fixes"""
        # Step 1: Code review
        review_result = agent.code_review(temp_buggy_file)
        assert review_result is not None

        review_text = str(review_result).lower()

        # Step 2: Check if issues were identified
        # Should mention division or zero or error handling
        has_issues = any(
            word in review_text
            for word in ["zero", "division", "error", "check", "validation", "bug"]
        )

        assert has_issues, "Code review should identify the bugs"

        # Step 3: Generate documentation
        docs_result = agent.generate_docs(temp_buggy_file)
        assert docs_result is not None

        docs_text = str(docs_result).lower()
        assert "divide" in docs_text or "process" in docs_text

    @pytest.mark.integration
    @pytest.mark.slow
    def test_multi_file_analysis(self, agent, tmp_path):
        """Test analyzing multiple related files"""
        # Create a simple module with multiple files
        (tmp_path / "utils.py").write_text(
            """
def helper_function():
    return "helper"
"""
        )

        (tmp_path / "main.py").write_text(
            """
from utils import helper_function

def main():
    print(helper_function())
"""
        )

        # Batch process
        results = agent.batch_process(
            str(tmp_path), "Describe what this file does", file_pattern="*.py"
        )

        assert len(results) == 2
        assert all(r["success"] for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
