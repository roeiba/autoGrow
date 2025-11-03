"""Tests for agent workflow"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Mock environment variables before importing
os.environ['GITHUB_TOKEN'] = 'test_token'
os.environ['ANTHROPIC_API_KEY'] = 'test_key'
os.environ['REPO_URL'] = 'https://github.com/test/repo'

from src.agent_workflow import AgentWorkflow


class TestAgentWorkflow:
    """Test suite for AgentWorkflow"""
    
    @pytest.fixture
    def workflow(self):
        """Create a workflow instance for testing"""
        with patch('src.agent_workflow.Github'), \
             patch('src.agent_workflow.Anthropic'):
            return AgentWorkflow()
    
    def test_initialization(self, workflow):
        """Test workflow initialization"""
        assert workflow.github_token == 'test_token'
        assert workflow.anthropic_api_key == 'test_key'
        assert workflow.repo_url == 'https://github.com/test/repo'
    
    def test_parse_repo_info(self, workflow):
        """Test repository URL parsing"""
        owner, repo = workflow._parse_repo_info()
        assert owner == 'test'
        assert repo == 'repo'
    
    def test_parse_repo_info_with_git_suffix(self):
        """Test parsing URL with .git suffix"""
        os.environ['REPO_URL'] = 'https://github.com/owner/name.git'
        with patch('src.agent_workflow.Github'), \
             patch('src.agent_workflow.Anthropic'):
            workflow = AgentWorkflow()
            owner, repo = workflow._parse_repo_info()
            assert owner == 'owner'
            assert repo == 'name'
    
    def test_validate_environment_missing_token(self):
        """Test validation with missing GitHub token"""
        os.environ.pop('GITHUB_TOKEN', None)
        
        with pytest.raises(ValueError, match="Missing required environment variables"):
            with patch('src.agent_workflow.Github'), \
                 patch('src.agent_workflow.Anthropic'):
                AgentWorkflow()
        
        # Restore for other tests
        os.environ['GITHUB_TOKEN'] = 'test_token'
    
    def test_analyze_codebase(self, workflow, tmp_path):
        """Test codebase analysis"""
        # Create test files
        (tmp_path / "test.py").touch()
        (tmp_path / "test.js").touch()
        (tmp_path / "requirements.txt").touch()
        
        workflow.repo_path = tmp_path
        analysis = workflow._analyze_codebase()
        
        assert 'py' in analysis['languages']
        assert 'js' in analysis['languages']
        assert 'requirements.txt' in analysis['key_files']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
