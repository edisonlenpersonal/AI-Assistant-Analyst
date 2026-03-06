"""
Planner Node

Creates step-by-step analysis plans based on dataset schema
and user questions.
"""

from app.utils.llm import call_llm
from app.utils.prompts import PLANNER_PROMPT


def create_analysis_plan(state: dict) -> dict:
    """
    Create a step-by-step analysis plan.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with analysis_plan
    """
    
    # Fill in the prompt template
    prompt = PLANNER_PROMPT.format(
        schema_info=state["schema_info"],
        sample_rows=state["sample_rows"],
        user_question=state["user_question"]
    )
    
    # Call Claude
    plan = call_llm(prompt, max_tokens=1024)
    
    # Update state
    state["analysis_plan"] = plan
    
    print("\n" + "=" * 50)
    print("📋 ANALYSIS PLAN GENERATED:")
    print("=" * 50)
    print(plan)
    
    return state


# Test independently
if __name__ == "__main__":
    test_state = {
        "schema_info": """Dataset Overview:
- Total Rows: 1,000
- Total Columns: 7

Column Details:
  • customer_id (int64): 1000 unique values
  • age (int64): 50 unique values, samples: [23, 45, 67]
  • gender (object): 2 unique values, samples: ['Male', 'Female']
  • tenure_months (int64): 72 unique values, samples: [1, 12, 48]
  • monthly_charges (float64): samples: [29.99, 89.50, 105.00]
  • total_charges (float64): samples: [29.99, 1200.00, 5000.00]
  • churn (object): 2 unique values, samples: ['Yes', 'No']""",
        
        "sample_rows": """| customer_id | age | gender | tenure_months | monthly_charges | churn |
|-------------|-----|--------|---------------|-----------------|-------|
| 1           | 34  | Male   | 12            | 65.5            | No    |
| 2           | 56  | Female | 45            | 89.2            | No    |
| 3           | 23  | Male   | 3             | 45.0            | Yes   |""",
        
        "user_question": "What factors are most associated with customer churn?"
    }
    
    result = create_analysis_plan(test_state)
    print("\n✅ Planner test complete!")