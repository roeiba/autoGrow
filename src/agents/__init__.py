"""
AI Agents Package

Core agent implementations for GitHub automation:
- IssueGenerator: Generates new issues using AI
- IssueResolver: Resolves issues and creates PRs
- QAAgent: Monitors repository health
"""

from .issue_generator import IssueGenerator
from .issue_resolver import IssueResolver
from .qa_agent import QAAgent

__all__ = ['IssueGenerator', 'IssueResolver', 'QAAgent']
