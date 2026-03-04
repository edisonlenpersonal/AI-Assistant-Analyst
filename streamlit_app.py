"""
DataLens AI - Streamlit Interface
==================================

A clean, professional UI for the autonomous data analysis agent.

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import json
import os
import tempfile
from datetime import datetime

# Must be the first Streamlit command
st.set_page_config(
    page_title="DataLens AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import our agent
from app.agent import run_analysis, create_agent, AgentState


def init_session_state():
    """Initialize session state variables."""
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
    if "results" not in st.session_state:
        st.session_state.results = None
    if "uploaded_file_path" not in st.session_state:
        st.session_state.uploaded_file_path = None


def save_uploaded_file(uploaded_file) -> str:
    """Save uploaded file to temp directory and return path."""
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Save with original filename
    file_path = os.path.join("data", uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path


def display_header():
    """Display the app header."""
    st.markdown("""
    # 📊 DataLens AI
    ### Autonomous Data Analysis Agent
    
    Upload your CSV file, ask a question, and let AI analyze your data.
    """)
    
    st.markdown("---")


def display_sidebar():
    """Display sidebar with instructions and info."""
    with st.sidebar:
        st.markdown("## How It Works")
        
        st.markdown("""
        **1. Upload** your CSV file
        
        **2. Ask** a question about your data
        
        **3. Watch** the AI analyze it:
        - 🔍 Schema Analysis
        - 📋 Planning
        - 💻 Code Generation
        - 🚀 Execution
        - 📝 Reporting
        
        **4. Get** insights and visualizations
        """)
        
        st.markdown("---")
        
        st.markdown("## About")
        st.markdown("""
        DataLens AI uses:
        - **Claude** for reasoning
        - **LangGraph** for orchestration
        - **Pandas** for analysis
        - **Plotly** for visualization
        """)
        
        st.markdown("---")
        
        st.markdown("## Sample Questions")
        st.markdown("""
        - *What factors influence churn?*
        - *Show me the distribution of sales by region*
        - *What are the trends over time?*
        - *Compare performance across categories*
        """)


def display_file_uploader():
    """Display file upload section."""
    st.markdown("### 📁 Step 1: Upload Your Data")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV file to analyze"
    )
    
    if uploaded_file is not None:
        # Save the file
        file_path = save_uploaded_file(uploaded_file)
        st.session_state.uploaded_file_path = file_path
        
        # Show preview
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        
        with st.expander("📋 Data Preview", expanded=True):
            df = pd.read_csv(file_path)
            st.dataframe(df.head(10), use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", f"{len(df):,}")
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                st.metric("Size", f"{uploaded_file.size / 1024:.1f} KB")
        
        return file_path
    
    return None


def display_question_input():
    """Display question input section."""
    st.markdown("### ❓ Step 2: Ask a Question")
    
    question = st.text_input(
        "What would you like to know about your data?",
        placeholder="e.g., What factors are most associated with customer churn?",
        help="Be specific about what you want to analyze"
    )
    
    return question


def run_analysis_with_progress(file_path: str, question: str):
    """Run analysis and display progress."""
    
    st.markdown("### ⚙️ Analysis in Progress")
    
    # Create progress container
    progress_container = st.container()
    
    with progress_container:
        # Progress steps
        steps = [
            ("🔍 Analyzing schema...", 0.1),
            ("📋 Creating analysis plan...", 0.3),
            ("💻 Generating code...", 0.5),
            ("🚀 Executing analysis...", 0.7),
            ("📝 Generating report...", 0.9),
        ]
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Show initial status
        status_text.text("Starting analysis...")
        
        # Simulate progress for each step
        import time
        for step_text, progress in steps:
            status_text.text(step_text)
            progress_bar.progress(progress)
            time.sleep(0.5)  # Brief pause for visual feedback
        
        # Actually run the analysis
        status_text.text("🔄 Processing...")
        
        try:
            results = run_analysis(file_path, question)
            progress_bar.progress(1.0)
            status_text.text("✅ Analysis complete!")
            
            return results
            
        except Exception as e:
            status_text.text("❌ Analysis failed")
            st.error(f"Error: {str(e)}")
            return None


def display_results(results: dict):
    """Display analysis results."""
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Tabs for different result sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Report", 
        "📊 Visualization", 
        "💻 Generated Code",
        "📋 Analysis Plan"
    ])
    
    # Tab 1: Report
    with tab1:
        st.markdown("### Final Report")
        st.markdown(results.get("final_report", "No report generated"))
        
        # Download button for report
        report_text = results.get("final_report", "")
        if report_text:
            st.download_button(
                label="📥 Download Report",
                data=report_text,
                file_name=f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
    
    # Tab 2: Visualization
    with tab2:
        st.markdown("### Generated Visualization")
        
        figure_json = results.get("figure_json", "")
        
        if figure_json:
            try:
                import plotly.io as pio
                fig = pio.from_json(figure_json)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display figure: {e}")
        else:
            st.info("No visualization was generated for this analysis.")
    
    # Tab 3: Generated Code
    with tab3:
        st.markdown("### Generated Python Code")
        
        code = results.get("generated_code", "")
        if code:
            st.code(code, language="python")
            
            # Download button for code
            st.download_button(
                label="📥 Download Code",
                data=code,
                file_name=f"analysis_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
                mime="text/plain"
            )
        else:
            st.info("No code was generated.")
    
    # Tab 4: Analysis Plan
    with tab4:
        st.markdown("### Analysis Plan")
        
        plan = results.get("analysis_plan", "")
        if plan:
            st.markdown(plan)
        else:
            st.info("No analysis plan available.")
        
        # Show schema info
        st.markdown("### Dataset Schema")
        schema = results.get("schema_info", "")
        if schema:
            st.text(schema)


def display_execution_details(results: dict):
    """Display execution details in an expander."""
    
    with st.expander("🔧 Execution Details", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Debug Attempts:**")
            st.write(results.get("debug_attempts", 0))
        
        with col2:
            st.markdown("**Execution Status:**")
            if results.get("execution_error"):
                st.error("Had errors (resolved)")
            else:
                st.success("Clean execution")
        
        # Execution output
        st.markdown("**Raw Execution Output:**")
        output = results.get("execution_result", "")
        if output:
            st.text(output[:2000] + "..." if len(output) > 2000 else output)


def main():
    """Main application entry point."""
    
    # Initialize session state
    init_session_state()
    
    # Display header and sidebar
    display_header()
    display_sidebar()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File upload
        file_path = display_file_uploader()
        
        # Question input
        if file_path:
            st.markdown("---")
            question = display_question_input()
            
            # Analyze button
            st.markdown("---")
            
            if st.button("🚀 Analyze Data", type="primary", use_container_width=True):
                if question:
                    with st.spinner("Running analysis..."):
                        results = run_analysis_with_progress(file_path, question)
                        
                        if results:
                            st.session_state.results = results
                            st.session_state.analysis_complete = True
                else:
                    st.warning("Please enter a question about your data.")
    
    # Display results if available
    if st.session_state.analysis_complete and st.session_state.results:
        display_results(st.session_state.results)
        display_execution_details(st.session_state.results)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Built with Claude + LangGraph + Streamlit | "
        "DataLens AI v1.0"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()