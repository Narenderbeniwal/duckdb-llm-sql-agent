# DuckDB + LLM SQL Agent

This project lets you query CSV data stored in **DuckDB** using **natural language**.  
It uses **LangChain SQL Agent + OpenAI LLMs** and provides a **Streamlit frontend** for interaction.

---

## Features
- Query CSV data in natural language  
- Handles chitchat & irrelevant queries gracefully  
- Runs SQL queries automatically via LLM  
- Shows results as tables and summaries  
- Auto-generates visualizations (pie, bar, histogram, scatter, line)  
- Streamlit frontend for easy use  

---

## Project Files
- `main.py` → Streamlit app (frontend)  
- `csv_to_duckdb_loader.py` → Loads CSVs into DuckDB  
- `agent_setup.py` → Initializes LLM SQL agent  
- `query_handler.py` → Handles queries, parsing, analysis  
- `visualization.py` → Creates charts  
- `requirements.txt` → Dependencies  
- `data/` → CSV files folder  

---

## Create Virtual Environment
python3 -m venv venv
source venv/bin/activate   # Mac/Linux

venv\Scripts\activate      # Windows
## Install Requirements
pip install -r requirements.txt
## Add OpenAI API Key
OPENAI_API_KEY=sk-xxxxxxx
## Run the App
streamlit run main.py
