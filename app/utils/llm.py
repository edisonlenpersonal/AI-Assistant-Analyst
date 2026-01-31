"""
LLM Utility
===========

Centralized Claude interaction for consistency.
"""

import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()


def get_llm(max_tokens: int = 4096):
    """
    Get a configured Claude instance.
    
    Args:
        max_tokens: Maximum tokens in response
        
    Returns:
        Configured ChatAnthropic instance
    """
    return ChatAnthropic(
        model="claude-sonnet-4-20250514",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=max_tokens
    )


def call_llm(prompt: str, max_tokens: int = 4096) -> str:
    """
    Make a simple call to Claude.
    
    Args:
        prompt: The prompt to send
        max_tokens: Maximum tokens in response
        
    Returns:
        Claude's response as a string
    """
    llm = get_llm(max_tokens)
    response = llm.invoke(prompt)
    return response.content