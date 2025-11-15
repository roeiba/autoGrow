"""
Anthropic API Helper Functions

Centralized utilities for calling Anthropic API with retry logic.
"""

from typing import Optional
from anthropic import Anthropic
from logging_config import get_logger
from utils.retry import retry_anthropic_api

logger = get_logger(__name__)


@retry_anthropic_api
def call_anthropic_api(
    api_key: str,
    prompt: str,
    model: str,
    max_tokens: int,
    system_prompt: Optional[str] = None
) -> str:
    """
    Call Anthropic API with retry logic
    
    Args:
        api_key: Anthropic API key
        prompt: User prompt/message
        model: Model name to use
        max_tokens: Maximum tokens in response
        system_prompt: Optional system prompt
    
    Returns:
        str: Response text from the API
    """
    client = Anthropic(api_key=api_key)
    
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    if system_prompt:
        kwargs["system"] = system_prompt
    
    message = client.messages.create(**kwargs)
    return message.content[0].text
