"""
DataLens AI - Autonomous Data Analysis Agent
=============================================

This agent takes natural language questions about data and:
1. Analyzes the dataset schema
2. Plans an analysis approach
3. Generates Python code
4. Executes code safely
5. Self-corrects on errors
6. Reports findings with visualizations
"""

from typing import TypedDict, Literal, Annotated
from langgraph.graph import StateGraph, START, END


# --- STATE DEFINITION ---
class AgentState(TypedDict):
    """
    The state that flows through our agent graph.
    
    This is the "shared memory" between all nodes.
    Each field serves a specific purpose in the pipeline.
    """
    
    # Input fields (set at the start)
    file_path: str              # Path to the uploaded CSV
    user_question: str          # What the user wants to know
    
    # Schema analysis output
    schema_info: str            # Structured description of the data
    column_types: dict          # Column name -> data type mapping
    sample_rows: str            # String representation of sample data
    
    # Planning output
    analysis_plan: str          # Step-by-step plan in natural language
    
    # Code generation output
    generated_code: str         # Python code to execute
    
    # Execution output
    execution_result: str       # Output from running the code
    execution_error: str        # Error message if execution failed
    figure_json: str            # Plotly figure as JSON (if visualization)
    
    # Debugging
    debug_attempts: int         # Number of debug attempts (max 3)
    
    # Final output
    final_report: str           # Human-readable analysis report