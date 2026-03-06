"""
Debugger Node

Analyzes execution errors and generates corrected code.
Implements self-correction loop with up to 3 retry attempts.
"""

from app.utils.llm import call_llm
from app.utils.prompts import DEBUGGER_PROMPT


def debug_code(state: dict) -> dict:
    """
    Analyze the error and fix the generated code.
    
    Args:
        state: Current agent state with execution_error
        
    Returns:
        Updated state with fixed generated_code and incremented debug_attempts
    """
    
    # Increment attempt counter
    attempts = state.get("debug_attempts", 0) + 1
    state["debug_attempts"] = attempts
    
    print("\n" + "=" * 50)
    print(f"🔧 DEBUGGING (Attempt {attempts}/3)")
    print("=" * 50)
    
    # Get error details
    error = state.get("execution_error", "Unknown error")
    original_code = state.get("generated_code", "")
    
    print(f"\n❌ Error to fix:\n{error[:300]}...")
    
    # Ask Claude to fix it
    prompt = DEBUGGER_PROMPT.format(
        generated_code=original_code,
        execution_error=error,
        schema_info=state.get("schema_info", "")
    )
    
    fixed_code = call_llm(prompt, max_tokens=2048)
    
    # Clean up the code
    fixed_code = clean_code_output(fixed_code)
    
    # Update state with fixed code
    state["generated_code"] = fixed_code
    
    # Clear the error so executor can try again
    state["execution_error"] = ""
    
    print("\n✅ Code fixed. Sending back to executor...")
    print("-" * 50)
    print(fixed_code[:500])
    if len(fixed_code) > 500:
        print("... (truncated)")
    
    return state


def clean_code_output(code: str) -> str:
    """Remove markdown code blocks if present."""
    if code.startswith("```python"):
        code = code[9:]
    elif code.startswith("```"):
        code = code[3:]
    
    if code.endswith("```"):
        code = code[:-3]
    
    return code.strip()


# Test independently
if __name__ == "__main__":
    test_state = {
        "generated_code": """
import pandas as pd
df = pd.read_csv('data/test_churn.csv')
print(df['nonexistent_column'].mean())
""",
        "execution_error": """Traceback (most recent call last):
  File "<string>", line 3, in <module>
KeyError: 'nonexistent_column'
""",
        "schema_info": """Column Details:
  • customer_id (int64)
  • age (int64)
  • gender (object)
  • tenure_months (int64)
  • monthly_charges (float64)
  • churn (object)""",
        "debug_attempts": 0
    }
    
    result = debug_code(test_state)
    print(f"\n\nDebug attempts: {result['debug_attempts']}")
    print(f"Fixed code:\n{result['generated_code']}")