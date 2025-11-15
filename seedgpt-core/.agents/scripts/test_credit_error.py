#!/usr/bin/env python3
"""
Test script to verify credit balance error handling
"""
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from utils.exceptions import (
    AgentError,
    CreditBalanceError,
    get_exception_for_anthropic_error,
)

def test_credit_balance_error():
    """Test that credit balance errors are properly detected and converted"""
    
    # Simulate the error from Claude CLI
    agent_error = AgentError(
        "Claude CLI credit balance is too low: Credit balance is too low\n\n",
        details={
            "returncode": 1,
            "stdout": "Credit balance is too low\n\n"
        }
    )
    
    print("Original AgentError:")
    print(f"  Message: {agent_error}")
    print(f"  Details: {agent_error.details}")
    print()
    
    # Convert it using the helper function
    converted_error = get_exception_for_anthropic_error(agent_error, "Failed to call Claude API")
    
    print("Converted Error:")
    print(f"  Type: {type(converted_error).__name__}")
    print(f"  Message: {converted_error}")
    print(f"  Is CreditBalanceError: {isinstance(converted_error, CreditBalanceError)}")
    
    if isinstance(converted_error, CreditBalanceError):
        print("✅ Credit balance error correctly detected!")
        print(f"  Service: {converted_error.service}")
    else:
        print("❌ Credit balance error NOT detected correctly")
        print(f"  Got: {type(converted_error).__name__}")
    
    return isinstance(converted_error, CreditBalanceError)

if __name__ == "__main__":
    success = test_credit_balance_error()
    sys.exit(0 if success else 1)
