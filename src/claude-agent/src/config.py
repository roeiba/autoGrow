"""Configuration management for Claude Agent"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class AgentConfig:
    """Agent configuration from environment variables"""
    
    github_token: str
    anthropic_api_key: str
    repo_url: str
    issue_number: Optional[int] = None
    agent_mode: str = "auto"
    workspace_path: str = "/workspace"
    prompt_template: str = "default"
    custom_prompt_path: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "AgentConfig":
        """Create configuration from environment variables"""
        issue_num = os.getenv('ISSUE_NUMBER')
        prompt_template = os.getenv('PROMPT_TEMPLATE', 'default')
        
        # Check if it's a file path or template name
        custom_prompt_path = None
        if prompt_template and (prompt_template.endswith('.txt') or '/' in prompt_template):
            custom_prompt_path = prompt_template
            prompt_template = 'custom'
        
        return cls(
            github_token=os.getenv('GITHUB_TOKEN', ''),
            anthropic_api_key=os.getenv('ANTHROPIC_API_KEY', ''),
            repo_url=os.getenv('REPO_URL', ''),
            issue_number=int(issue_num) if issue_num else None,
            agent_mode=os.getenv('AGENT_MODE', 'auto'),
            workspace_path=os.getenv('WORKSPACE_PATH', '/workspace'),
            prompt_template=prompt_template,
            custom_prompt_path=custom_prompt_path
        )
    
    def validate(self) -> None:
        """Validate required configuration"""
        required = {
            'github_token': self.github_token,
            'anthropic_api_key': self.anthropic_api_key,
            'repo_url': self.repo_url
        }
        
        missing = [k for k, v in required.items() if not v]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
    
    @property
    def is_dry_run(self) -> bool:
        """Check if running in dry-run mode"""
        return self.agent_mode == 'dry-run'
