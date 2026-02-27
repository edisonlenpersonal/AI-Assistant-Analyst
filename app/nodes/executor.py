"""
Executor Node
=============

This node runs the generated Python code and captures:
- Output (print statements)
- Errors (if any)
- Figures (Plotly visualizations)

If execution fails, the error is stored so the Debugger can fix it.
"""

from app.tools.code_executor import execute_code_safely


def execute_analysis_code(state: dict) -> dict:
    """
    Execute the generated analysis code.
    
    Args:
        state: Current agent state with 'generated_code'
        
    Returns:
        Updated state with execution_result, execution_error, figure_json
    """
    
    code = state.get("generated_code", "")
    
    if not code:
        state["execution_error"] = "No code to execute"
        state["execution_result"] = ""
        return state
    
    print("\n" + "=" * 50)
    print("🚀 EXECUTING CODE...")
    print("=" * 50)
    
    # Execute the code
    output, error, figure_json = execute_code_safely(code)
    
    # Update state
    state["execution_result"] = output
    state["execution_error"] = error
    state["figure_json"] = figure_json if figure_json else ""
    
    # Print status
    if error:
        print("\n❌ EXECUTION FAILED:")
        print("-" * 50)
        print(error[:500])  # First 500 chars of error
        if len(error) > 500:
            print("... (error truncated)")
    else:
        print("\n✅ EXECUTION SUCCESSFUL:")
        print("-" * 50)
        print(output[:1000] if len(output) > 1000 else output)
        if figure_json:
            print("\n📊 Plotly figure generated!")
    
    return state


# Keep the old name for backward compatibility with agent.py
def execute_code(state: dict) -> dict:
    """Wrapper to maintain compatibility."""
    return execute_analysis_code(state)


# Test independently
if __name__ == "__main__":
    # Test with working code
    print("TEST 1: Working code")
    test_state = {
        "generated_code": """
import pandas as pd
print("Loading data...")
df = pd.DataFrame({'a': [1,2,3], 'b': [4,5,6]})
print(f"Data shape: {df.shape}")
print(df)
"""
    }
    
    result = execute_analysis_code(test_state)
    print(f"\nExecution result: {result['execution_result']}")
    print(f"Error: {result['execution_error'] if result['execution_error'] else 'None'}")
    
    # Test with broken code
    print("\n" + "=" * 50)
    print("TEST 2: Broken code")
    test_state_2 = {
        "generated_code": """
import pandas as pd
df = pd.read_csv('nonexistent_file.csv')
print(df)
"""
    }
    
    result = execute_analysis_code(test_state_2)
    print(f"\nHas error: {bool(result['execution_error'])}")