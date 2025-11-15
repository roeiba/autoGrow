"""Configuration management for Claude Agent using pydantic-settings"""

import sys
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

sys.path.insert(0, str(Path(__file__).parent.parent))
from logging_config import get_logger

logger = get_logger(__name__)


class AgentConfig(BaseSettings):
    """Agent configuration with environment variable support and validation

    Supports multiple configuration sources with priority:
    1. Environment variables (highest priority)
    2. .env file
    3. Default values (lowest priority)
    """

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Required fields
    github_token: str = Field(..., description="GitHub personal access token")
    anthropic_api_key: str = Field(..., description="Anthropic API key for Claude")
    repo_url: str = Field(..., description="Repository URL")

    # Optional fields with defaults
    issue_number: Optional[int] = Field(
        None, description="Specific issue number to resolve"
    )
    agent_mode: str = Field("auto", description="Agent mode: auto, dry-run, or manual")
    workspace_path: str = Field("/workspace", description="Workspace directory path")
    prompt_template: str = Field("default", description="Prompt template name or path")
    custom_prompt_path: Optional[str] = Field(
        None, description="Custom prompt file path"
    )

    @field_validator("prompt_template", mode="before")
    @classmethod
    def parse_prompt_template(cls, v):
        """Parse prompt template and extract custom path if needed"""
        if v and (v.endswith(".txt") or "/" in v):
            return "custom"
        return v or "default"

    @field_validator("agent_mode")
    @classmethod
    def validate_agent_mode(cls, v):
        """Validate agent mode is one of allowed values"""
        allowed = {"auto", "dry-run", "manual"}
        if v not in allowed:
            raise ValueError(f"agent_mode must be one of {allowed}, got: {v}")
        return v

    @property
    def is_dry_run(self) -> bool:
        """Check if running in dry-run mode"""
        return self.agent_mode == "dry-run"
