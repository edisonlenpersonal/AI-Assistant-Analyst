"""
Reporter Node
=============

This node transforms raw analysis output into a polished report.

Why this matters:
- Raw code output is messy (debug prints, technical jargon)
- Users want clear answers, not code logs
- Good reporting shows business value, not just technical work

This is what separates a demo from a product.
"""

from app.utils.llm import call_llm
from app.utils.prompts import REPORTER_PROMPT


def generate_report(state: dict) -> dict:
    """
    Generate a human-readable analysis report.
    
    Args:
        state: Current agent state with execution_result
        
    Returns:
        Updated state with final_report
    """
    
    print("\n" + "=" * 50)
    print("📝 GENERATING REPORT...")
    print("=" * 50)
    
    # Check if we have results to report on
    execution_result = state.get("execution_result", "")
    execution_error = state.get("execution_error", "")
    
    # If there was an unresolved error, report that
    if execution_error and not execution_result:
        state["final_report"] = generate_error_report(state)
        return state
    
    # Generate the report using Claude
    prompt = REPORTER_PROMPT.format(
        user_question=state.get("user_question", "Analyze this data"),
        execution_result=execution_result[:8000]  # Limit context size
    )
    
    report = call_llm(prompt, max_tokens=2048)
    
    # Store the report
    state["final_report"] = report
    
    print("\n✅ Report generated successfully!")
    print("-" * 50)
    print(report[:1000])
    if len(report) > 1000:
        print("... (truncated for display)")
    
    return state


def generate_error_report(state: dict) -> str:
    """
    Generate a report explaining that analysis failed.
    
    Args:
        state: Current agent state
        
    Returns:
        Error report string
    """
    error = state.get("execution_error", "Unknown error")
    question = state.get("user_question", "your question")
    attempts = state.get("debug_attempts", 0)
    
    report = f"""## Analysis Report

### Status: ⚠️ Analysis Incomplete

I attempted to analyze your data to answer: **"{question}"**

Unfortunately, the analysis encountered technical issues that couldn't be automatically resolved after {attempts} attempts.

### Error Summary
```
{error[:500]}
```

### Recommendations
1. **Check your data file** - Ensure the CSV is properly formatted
2. **Simplify your question** - Try a more specific query
3. **Review column names** - Make sure referenced columns exist

### What Was Attempted
{state.get('analysis_plan', 'No plan generated')}

---
*This report was generated automatically. Please try again or rephrase your question.*
"""
    
    return report


# Test independently
if __name__ == "__main__":
    # Test with successful execution
    print("TEST 1: Successful execution report")
    print("=" * 50)
    
    test_state = {
        "user_question": "What factors influence customer churn?",
        "execution_result": """
Loading data...
Data loaded successfully. Shape: (5, 7)

==================================================
STEP 1: CHECKING FOR MISSING VALUES
==================================================
Missing values by column:
churn: 0
age: 0
tenure_months: 0

==================================================
STEP 2: CHURN RATES BY DEMOGRAPHIC SEGMENTS
==================================================
Churn rate by gender:
Male: 66.67%
Female: 0.0%

Churn rate by age group:
18-30: 100.0%
31-50: 50.0%
50+: 0.0%

==================================================
KEY INSIGHTS
==================================================
Overall churn rate: 40.0% (2/5 customers)
Most important numerical factor: tenure_months
Strongest correlation: 0.945

Churned customers have:
- tenure_months: -30.17 (lower for churned customers)
- monthly_charges: -29.40 (lower for churned customers)
- age: -21.33 (lower for churned customers)
""",
        "execution_error": "",
        "analysis_plan": "1. Check missing values\n2. Calculate churn rates\n3. Identify key factors"
    }
    
    result = generate_report(test_state)
    print(f"\n\nFull report:\n{result['final_report']}")
    
    # Test with failed execution
    print("\n\n" + "=" * 50)
    print("TEST 2: Failed execution report")
    print("=" * 50)
    
    test_state_error = {
        "user_question": "What factors influence customer churn?",
        "execution_result": "",
        "execution_error": "KeyError: 'nonexistent_column'",
        "analysis_plan": "1. Load data\n2. Analyze columns",
        "debug_attempts": 3
    }
    
    result = generate_report(test_state_error)
    print(f"\n\nError report:\n{result['final_report']}")