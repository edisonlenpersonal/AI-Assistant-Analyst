"""
Coder Node
==========

This node generates Python code based on:
1. The analysis plan from the Planner
2. The dataset schema
3. The user's question

The code will be executed in the next node.
"""

from app.utils.llm import call_llm
from app.utils.prompts import CODER_PROMPT


def generate_code(state: dict) -> dict:
    """
    Generate Python code to perform the analysis.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with generated_code
    """
    
    # Fill in the prompt template
    prompt = CODER_PROMPT.format(
        schema_info=state["schema_info"],
        sample_rows=state["sample_rows"],
        analysis_plan=state["analysis_plan"],
        user_question=state["user_question"],
        file_path=state["file_path"]
    )
    
    # Call Claude
    code = call_llm(prompt, max_tokens=2048)
    
    # Clean up the code (remove markdown if present)
    code = clean_code_output(code)
    
    # Update state
    state["generated_code"] = code
    
    print("\n" + "=" * 50)
    print("💻 GENERATED CODE:")
    print("=" * 50)
    print(code)
    
    return state


def clean_code_output(code: str) -> str:
    """
    Clean up LLM code output.
    
    Sometimes Claude wraps code in markdown blocks despite instructions.
    This removes that wrapping.
    """
    # Remove markdown code blocks if present
    if code.startswith("```python"):
        code = code[9:]  # Remove ```python
    elif code.startswith("```"):
        code = code[3:]  # Remove ```
    
    if code.endswith("```"):
        code = code[:-3]  # Remove trailing ```
    
    return code.strip()


# Test independently
if __name__ == "__main__":
    test_state = {
        "file_path": "data/test_churn.csv",
        
        "schema_info": """Dataset Overview:
- Total Rows: 5
- Total Columns: 7

Column Details:
  • customer_id (int64): unique identifier
  • age (int64): customer age
  • gender (object): Male/Female
  • tenure_months (int64): months as customer
  • monthly_charges (float64): monthly bill amount
  • total_charges (float64): total amount paid
  • churn (object): Yes/No - did customer leave""",
        
        "sample_rows": """| customer_id | age | gender | tenure_months | monthly_charges | churn |
|-------------|-----|--------|---------------|-----------------|-------|
| 1           | 34  | Male   | 12            | 65.5            | No    |
| 2           | 56  | Female | 45            | 89.2            | No    |""",
        
        "analysis_plan": """1. Load the data and check the churn distribution
2. Compare average tenure_months between churned and non-churned customers
3. Compare average monthly_charges between groups
4. Create a bar chart showing churn rate by different factors
5. Summarize the key differences""",
        
        "user_question": "What factors are most associated with customer churn?"
    }
    
    result = generate_code(test_state)
    print("\n✅ Coder test complete!")