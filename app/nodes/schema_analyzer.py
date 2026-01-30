"""
Schema Analyzer Node
====================

This node is the "eyes" of our agent. It:
1. Loads the CSV file
2. Extracts column names and types
3. Gets sample rows
4. Creates a structured summary for the LLM

Why this matters:
- LLMs can't "see" files directly
- We need to convert data structure into text
- Good schema description = better code generation
"""

import pandas as pd
from tabulate import tabulate


def analyze_schema(state: dict) -> dict:
    """
    Analyze the uploaded CSV file and extract schema information.
    
    Args:
        state: Current agent state with 'file_path'
        
    Returns:
        Updated state with schema_info, column_types, sample_rows
    """
    
    file_path = state["file_path"]
    
    # Load the CSV
    df = pd.read_csv(file_path)
    
    # --- Extract Column Information ---
    column_info = []
    column_types = {}
    
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].notna().sum()
        total = len(df)
        unique = df[col].nunique()
        
        # Get sample values (first 3 unique non-null values)
        sample_values = df[col].dropna().unique()[:3].tolist()
        
        column_info.append({
            "column": col,
            "dtype": dtype,
            "non_null": f"{non_null}/{total}",
            "unique": unique,
            "samples": sample_values
        })
        
        column_types[col] = dtype
    
    # --- Create Schema Summary ---
    schema_lines = [
        f"Dataset Overview:",
        f"- Total Rows: {len(df):,}",
        f"- Total Columns: {len(df.columns)}",
        f"",
        f"Column Details:",
    ]
    
    for info in column_info:
        schema_lines.append(
            f"  • {info['column']} ({info['dtype']}): "
            f"{info['unique']} unique values, "
            f"samples: {info['samples']}"
        )
    
    schema_info = "\n".join(schema_lines)
    
    # --- Get Sample Rows ---
    sample_df = df.head(5)
    sample_rows = tabulate(sample_df, headers='keys', tablefmt='pipe', showindex=False)
    
    # --- Update State ---
    state["schema_info"] = schema_info
    state["column_types"] = column_types
    state["sample_rows"] = sample_rows
    
    return state


# --- Test the node independently ---
if __name__ == "__main__":
    import os
    
    test_data = """customer_id,age,gender,tenure_months,monthly_charges,total_charges,churn
1,34,Male,12,65.5,786.0,No
2,56,Female,45,89.2,4014.0,No
3,23,Male,3,45.0,135.0,Yes
4,67,Female,67,112.5,7537.5,No
5,45,Male,8,78.3,626.4,Yes"""
    
    os.makedirs("data", exist_ok=True)
    with open("data/test_churn.csv", "w") as f:
        f.write(test_data)
    
    test_state = {
        "file_path": "data/test_churn.csv",
        "user_question": "What factors influence churn?"
    }
    
    result = analyze_schema(test_state)
    
    print("=" * 50)
    print("SCHEMA INFO:")
    print("=" * 50)
    print(result["schema_info"])
    print("\n" + "=" * 50)
    print("SAMPLE ROWS:")
    print("=" * 50)
    print(result["sample_rows"])