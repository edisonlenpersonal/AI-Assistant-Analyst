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

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

from app.nodes import (
    analyze_schema,
    create_analysis_plan,
    generate_code,
    execute_code,
    debug_code,
    generate_report
)


# --- STATE DEFINITION ---
class AgentState(TypedDict):
    """
    The state that flows through our agent graph.
    
    Think of this as a "baton" in a relay race that accumulates
    information as it passes through each node.
    """
    
    # Input
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


# --- ROUTING FUNCTIONS ---
def should_debug(state: AgentState) -> Literal["debug", "report"]:
    """
    Decide whether to debug or proceed to reporting.
    
    This is the KEY to self-correction:
    - If there's an error AND we haven't tried 3 times -> debug
    - Otherwise -> proceed to report
    """
    has_error = bool(state.get("execution_error"))
    attempts = state.get("debug_attempts", 0)
    
    if has_error and attempts < 3:
        return "debug"
    else:
        return "report"


# --- BUILD THE GRAPH ---
def create_agent():
    """
    Create the DataLens AI agent graph.
    
    Flow:
    START -> schema_analyzer -> planner -> coder -> executor
                                                        |
                                                (check for errors)
                                                        |
                                            +-----------+-----------+
                                            |                       |
                                            v                       v
                                        [debug]                 [report]
                                            |                       |
                                            v                       v
                                        executor                   END
    """
    
    workflow = StateGraph(AgentState)
    
    # Add all nodes
    workflow.add_node("schema_analyzer", analyze_schema)
    workflow.add_node("planner", create_analysis_plan)
    workflow.add_node("coder", generate_code)
    workflow.add_node("executor", execute_code)
    workflow.add_node("debugger", debug_code)
    workflow.add_node("reporter", generate_report)
    
    # Define the flow
    workflow.add_edge(START, "schema_analyzer")
    workflow.add_edge("schema_analyzer", "planner")
    workflow.add_edge("planner", "coder")
    workflow.add_edge("coder", "executor")
    
    # Conditional routing after execution
    workflow.add_conditional_edges(
        "executor",
        should_debug,
        {
            "debug": "debugger",
            "report": "reporter"
        }
    )
    
    # Debugger goes back to executor to retry
    workflow.add_edge("debugger", "executor")
    
    # Reporter ends the flow
    workflow.add_edge("reporter", END)
    
    return workflow.compile()


def run_analysis(file_path: str, question: str) -> dict:
    """
    Run the DataLens AI agent on a dataset.
    
    Args:
        file_path: Path to the CSV file
        question: User's analysis question
        
    Returns:
        Final agent state with results
    """
    agent = create_agent()
    
    initial_state = {
        "file_path": file_path,
        "user_question": question,
        "schema_info": "",
        "column_types": {},
        "sample_rows": "",
        "analysis_plan": "",
        "generated_code": "",
        "execution_result": "",
        "execution_error": "",
        "figure_json": "",
        "debug_attempts": 0,
        "final_report": ""
    }
    
    final_state = agent.invoke(initial_state)
    
    return final_state


# --- TEST ---
if __name__ == "__main__":
    import os
    
    print("Testing DataLens AI Agent (Phase 1)...\n")
    
    # Create test data
    test_csv = """customer_id,age,gender,tenure_months,monthly_charges,total_charges,churn
1,34,Male,12,65.5,786.0,No
2,56,Female,45,89.2,4014.0,No
3,23,Male,3,45.0,135.0,Yes
4,67,Female,67,112.5,7537.5,No
5,45,Male,8,78.3,626.4,Yes"""
    
    os.makedirs("data", exist_ok=True)
    with open("data/test_churn.csv", "w") as f:
        f.write(test_csv)
    
    # Run the agent
    result = run_analysis(
        file_path="data/test_churn.csv",
        question="What factors influence customer churn?"
    )
    
    print("=" * 50)
    print("SCHEMA INFO:")
    print("=" * 50)
    print(result["schema_info"])
    
    print("\n" + "=" * 50)
    print("SAMPLE ROWS:")
    print("=" * 50)
    print(result["sample_rows"])
    
    print("\n" + "=" * 50)
    print("ANALYSIS PLAN:")
    print("=" * 50)
    print(result["analysis_plan"])
    
    print("\n" + "=" * 50)
    print("FINAL REPORT:")
    print("=" * 50)
    print(result["final_report"])
    
    print("\n✅ Phase 1 Complete!")