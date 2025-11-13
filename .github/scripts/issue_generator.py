#!/usr/bin/env python3
"""
Issue Generator Agent - GitHub Actions Wrapper

Thin wrapper script for GitHub Actions workflows.
Core logic is in src/agents/issue_generator.py
"""

import os
import sys
from pathlib import Path
from github import Github, Auth

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

# Import core agent
from agents.issue_generator import IssueGenerator

# Configuration from environment
MIN_ISSUES = int(os.getenv('MIN_OPEN_ISSUES', '3'))
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
REPO_NAME = os.getenv('REPO_NAME')

if not GITHUB_TOKEN or not REPO_NAME:
    print("❌ Missing required environment variables: GITHUB_TOKEN, REPO_NAME")
    sys.exit(1)

# Initialize GitHub client
auth = Auth.Token(GITHUB_TOKEN)
gh = Github(auth=auth)
repo = gh.get_repo(REPO_NAME)

print(f"✅ Connected to repository: {REPO_NAME}")

# Run the agent
try:
    agent = IssueGenerator(
        repo=repo,
        anthropic_api_key=ANTHROPIC_API_KEY,
        min_issues=MIN_ISSUES
    )
    
    agent.check_and_generate()
    
except Exception as e:
    print(f"❌ Fatal error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
