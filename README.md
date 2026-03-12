# 📊 DataLens AI

An autonomous data analysis agent that answers questions about your data using natural language.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Claude](https://img.shields.io/badge/LLM-Claude-orange.svg)
![LangGraph](https://img.shields.io/badge/Framework-LangGraph-green.svg)

## 🎯 What It Does

Upload a CSV, ask a question, get insights.
```
You: "What factors influence customer churn?"

DataLens AI:
1. Analyzes your data schema
2. Creates an analysis plan
3. Generates Python code
4. Executes the analysis
5. Self-corrects if errors occur
6. Delivers a polished report with visualizations
```

## 🏗️ Architecture
```
┌────────────────────────────────────────────────────────────┐
│                       STREAMLIT UI                         │
│         Upload CSV → Ask Question → View Results           │
└────────────────────────────┬───────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────┐
│                     LANGGRAPH AGENT                        │
│                                                            │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌──────────┐   │
│   │ Schema  │ → │ Planner │ → │  Coder  │ → │ Executor │   │
│   │Analyzer │   │         │   │         │   │          │   │
│   └─────────┘   └─────────┘   └─────────┘   └────┬─────┘   │
│                                                  │         │
│                                           ┌──────┴──────┐  │
│                                           │  Has Error? │  │
│                                           └──────┬──────┘  │
│                                          Yes │       │ No  │
│                                              ▼       ▼     │
│                                        ┌────────┐ ┌──────┐ │
│                                        │Debugger│ │Report│ │
│                                        └───┬────┘ └──┬───┘ │
│                                            │         │     │
│                                            ▼         ▼     │
│                                       [Executor]    END    │
└────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/edisonlenpersonal/AI-Assistant-Analyst
cd datalens-ai

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Add API Key

Create `.env` file:
```
ANTHROPIC_API_KEY=your_key_here
```

### 3. Run
```bash
streamlit run streamlit_app.py
```

## 🧠 Key Features

| Feature | Description |
|---------|-------------|
| **Natural Language Queries** | Ask questions in plain English |
| **Autonomous Analysis** | AI plans and executes analysis without manual coding |
| **Self-Correction** | Automatically fixes code errors (up to 3 attempts) |
| **Visualizations** | Generates interactive Plotly charts |
| **Professional Reports** | Delivers business-ready insights |

## 🛠️ Tech Stack

- **LLM**: Claude (Anthropic)
- **Agent Framework**: LangGraph
- **Data Processing**: Pandas, DuckDB
- **Visualization**: Plotly
- **UI**: Streamlit
- **Vector Store**: ChromaDB (for RAG features)

## 📁 Project Structure
```
datalens-ai/
├── app/
│   ├── agent.py              # Main LangGraph agent
│   ├── nodes/                # Processing nodes
│   │   ├── schema_analyzer.py
│   │   ├── planner.py
│   │   ├── coder.py
│   │   ├── executor.py
│   │   ├── debugger.py
│   │   └── reporter.py
│   ├── tools/
│   │   └── code_executor.py  # Safe code execution
│   └── utils/
│       ├── prompts.py        # LLM prompts
│       └── llm.py            # Claude interface
├── streamlit_app.py          # Web UI
├── requirements.txt
└── README.md
```

## 📊 Example Usage

**Input:**
- File: `customer_data.csv`
- Question: "What factors are most associated with customer churn?"

**Output:**
- Analysis plan (6 steps)
- Python code (~150 lines)
- Interactive visualizations
- Professional report with insights


## 📝 License

MIT License - feel free to use for your own portfolio!

## 🤝 Contact

- GitHub: [My Github](https://github.com/edisonlenpersonal/AI-Assistant-Analyst)
- LinkedIn: [My linkedin](https://www.linkedin.com/in/edison-len/)
- Email: edisonlen02128@gmail.com