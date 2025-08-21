# main.py

import os
import streamlit as st
import pandas as pd

from csv_to_duckdb_loader import db   # DuckDB + LangChain wrapper
from agent_setup import init_agent
from query_handler import query_db    # using query_handler.py directly
from visualization import auto_visualize   # visualization module

# --- Set your OpenAI key safely (prefer Streamlit secrets in production)
os.environ["OPENAI_API_KEY"] = ""
# --- Streamlit page setup
st.set_page_config(page_title="DuckDB + LLM SQL Agent", layout="wide")

def main():
    # Initialize the agent
    llm, agent_executor = init_agent(db)

    st.title("🦜🔗 DuckDB + LLM SQL Agent")
    st.markdown("Query your **CSV data in DuckDB** using natural language.")

    # Input box for user query
    user_input = st.text_input("💬 Enter your query:", "")

    if user_input:
        with st.spinner("Processing your query..."):
            try:
                result = query_db(user_input, llm, agent_executor, visualize=False)

                # If result is a DataFrame
                if isinstance(result, pd.DataFrame) and not result.empty:
                    st.subheader("📊 Query Result")
                    st.dataframe(result)

                    st.subheader("📈 Data Summary")
                    st.write(result.describe(include='all'))

                    # --- Auto Visualizations ---
                    st.subheader("📊 Visualizations")
                    figs = auto_visualize(result, return_figs=True)
                    if figs:
                        for fig in figs:
                            st.pyplot(fig)
                    else:
                        st.info("No suitable visualization generated for this query.")

                # If result is plain text
                elif isinstance(result, str):
                    st.subheader("📝 Query Response")
                    st.write(result)

                else:
                    st.warning("No structured result returned.")

            except Exception as e:
                st.error(f"❌ Error while processing query: {e}")

if __name__ == "__main__":
    main()
