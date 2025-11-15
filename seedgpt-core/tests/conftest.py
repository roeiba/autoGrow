"""
Pytest configuration and shared fixtures
"""

import pytest
import os
import sys
from pathlib import Path

# Add src directories to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root / "src" / "gemini-agent"))
sys.path.insert(0, str(project_root / "src" / "claude-agent"))


@pytest.fixture
def project_root():
    """Return the project root directory"""
    return Path(__file__).parent.parent


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Fixture to mock environment variables"""

    def _set_env(**kwargs):
        for key, value in kwargs.items():
            monkeypatch.setenv(key, value)

    return _set_env


@pytest.fixture
def clean_env(monkeypatch):
    """Fixture to provide clean environment"""
    # Remove common API keys from environment
    keys_to_remove = [
        "GEMINI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GITHUB_TOKEN",
        "GOOGLE_API_KEY",
        "GOOGLE_CLOUD_PROJECT",
    ]
    for key in keys_to_remove:
        monkeypatch.delenv(key, raising=False)


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test (requires external services)",
    )
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line(
        "markers", "requires_api_key: mark test as requiring API key"
    )
