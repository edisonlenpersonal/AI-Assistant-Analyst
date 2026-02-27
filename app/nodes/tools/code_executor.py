"""
Code Executor Tool
==================

Safely executes generated Python code and captures:
- Standard output (print statements)
- Errors and exceptions
- Plotly figures (for visualization)

Safety note: This executes arbitrary code. In production,
you'd want to run this in a sandboxed environment (Docker, E2B, etc.)
For this portfolio project, we run locally with basic precautions.
"""

import sys
import io
import traceback
from typing import Tuple, Optional
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def execute_code(code: str) -> Tuple[str, str, Optional[str]]:
    """
    Execute Python code and capture results.
    
    Args:
        code: Python code string to execute
        
    Returns:
        Tuple of (output, error, figure_json)
        - output: Captured print statements
        - error: Error message if execution failed, empty string if success
        - figure_json: Plotly figure as JSON string, None if no figure
    """
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    # Variables to store results
    error_message = ""
    figure_json = None
    
    # Create execution namespace with common imports pre-loaded
    exec_namespace = {
        "pd": pd,
        "np": np,
        "px": px,
        "go": go,
        "make_subplots": make_subplots,
        "__builtins__": __builtins__,
    }
    
    try:
        # Execute the code
        exec(code, exec_namespace)
        
        # Check if a figure was created
        if "fig" in exec_namespace:
            fig = exec_namespace["fig"]
            if hasattr(fig, "to_json"):
                figure_json = fig.to_json()
                
    except Exception as e:
        # Capture the full traceback
        error_message = traceback.format_exc()
        
    finally:
        # Restore stdout
        sys.stdout = old_stdout
    
    # Get captured output
    output = captured_output.getvalue()
    
    return output, error_message, figure_json


def execute_code_safely(code: str, timeout_seconds: int = 30) -> Tuple[str, str, Optional[str]]:
    """
    Execute code with additional safety measures.
    
    For portfolio purposes, this is a simple wrapper.
    In production, you'd add:
    - Timeout enforcement
    - Memory limits
    - Sandboxed execution (Docker/E2B)
    - Blocked imports (os, subprocess, etc.)
    
    Args:
        code: Python code to execute
        timeout_seconds: Max execution time (not enforced in this version)
        
    Returns:
        Tuple of (output, error, figure_json)
    """
    
    # Basic code validation
    dangerous_patterns = [
        "import os",
        "import subprocess",
        "import sys",
        "open(",
        "__import__",
        "eval(",
        "exec(",
    ]
    
    # Note: We're not blocking these, just flagging for awareness
    # A production system would reject code with these patterns
    for pattern in dangerous_patterns:
        if pattern in code:
            print(f"Warning: Code contains potentially dangerous pattern: {pattern}")
    
    return execute_code(code)


# Test the executor
if __name__ == "__main__":
    # Test 1: Simple code
    print("=" * 50)
    print("TEST 1: Simple print statement")
    print("=" * 50)
    
    test_code_1 = """
print("Hello from executed code!")
x = 5 + 3
print(f"5 + 3 = {x}")
"""
    
    output, error, fig = execute_code(test_code_1)
    print(f"Output:\n{output}")
    print(f"Error: {error if error else 'None'}")
    
    # Test 2: Code with error
    print("\n" + "=" * 50)
    print("TEST 2: Code with error")
    print("=" * 50)
    
    test_code_2 = """
print("Starting...")
x = undefined_variable
print("This won't print")
"""
    
    output, error, fig = execute_code(test_code_2)
    print(f"Output:\n{output}")
    print(f"Error:\n{error}")
    
    # Test 3: Code with Plotly figure
    print("\n" + "=" * 50)
    print("TEST 3: Code with Plotly figure")
    print("=" * 50)
    
    test_code_3 = """
import plotly.express as px
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
print("Figure created successfully!")
"""
    
    output, error, fig = execute_code(test_code_3)
    print(f"Output:\n{output}")
    print(f"Error: {error if error else 'None'}")
    print(f"Figure JSON exists: {fig is not None}")
    
    print("\n✅ Executor tests complete!")