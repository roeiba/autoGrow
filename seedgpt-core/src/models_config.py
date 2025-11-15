"""
Centralized AI Models Configuration

This module contains all AI model configurations used across the project.
All model names, parameters, and settings should be defined here.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ClaudeModels:
    """Claude AI model configurations"""

    # Primary models
    SONNET_3_5 = "claude-3-5-sonnet-20241022"
    SONNET_4_5 = "claude-sonnet-4-5"

    # Default model for different use cases
    DEFAULT = SONNET_3_5
    ISSUE_GENERATION = SONNET_3_5
    QA_ANALYSIS = SONNET_3_5
    ISSUE_RESOLUTION = SONNET_3_5
    WORKFLOW = SONNET_3_5

    # Model parameters
    DEFAULT_MAX_TOKENS = 2000
    QA_MAX_TOKENS = 3000
    WORKFLOW_MAX_TOKENS = 4096


@dataclass
class GeminiModels:
    """Gemini AI model configurations"""

    # Primary models
    PRO = "gemini-pro"
    PRO_VISION = "gemini-pro-vision"

    # Default model
    DEFAULT = PRO


@dataclass
class ModelConfig:
    """Main model configuration class"""

    def __init__(self):
        self.claude = ClaudeModels()
        self.gemini = GeminiModels()

    @staticmethod
    def get_anthropic_api_key() -> Optional[str]:
        """Get Anthropic API key from environment"""
        return os.getenv("ANTHROPIC_API_KEY")

    @staticmethod
    def get_gemini_api_key() -> Optional[str]:
        """Get Gemini API key from environment"""
        return os.getenv("GEMINI_API_KEY")

    @staticmethod
    def use_claude_cli() -> bool:
        """Check if Claude CLI should be used instead of API"""
        return os.getenv("USE_CLAUDE_CLI", "false").lower() == "true"


# Global instance
MODELS = ModelConfig()


# Convenience exports
CLAUDE_MODELS = MODELS.claude
GEMINI_MODELS = MODELS.gemini


# System prompts
class SystemPrompts:
    """Centralized system prompts for different agents"""

    ISSUE_GENERATOR = (
        "You are a helpful GitHub issue generator. Always respond with valid JSON only."
    )
    QA_ENGINEER = "You are a QA engineer. Always respond with valid JSON only."
    ISSUE_RESOLVER = "You are an expert software engineer. Fix this GitHub issue by modifying the necessary files."
