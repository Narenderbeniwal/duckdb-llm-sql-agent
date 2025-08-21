import re
import pandas as pd
from io import StringIO
import streamlit as st
from visualization import auto_visualize

def query_db(prompt: str, llm, agent_executor, visualize=True):
    chitchat_keywords = ["hello", "hi", "how are you", "good morning", "good evening", "thanks", "thank you"]
    irrelevant_keywords = ["weather", "football", "cricket", "politics", "movie", "music", "joke"]

    lower_prompt = prompt.lower()

    # Handle chitchat
    if any(word in lower_prompt for word in chitchat_keywords):
        st.info("🤖 Hello! How can I assist you with sales, customers, products, employees, cities, or countries data today?")
        return None

    # Handle irrelevant queries
    if any(word in lower_prompt for word in irrelevant_keywords):
        st.warning("🤖 Sorry, I can only answer questions related to sales, customers, products, employees, cities, or countries.")
        return None

    # Run LLM agent
    result = agent_executor.invoke({"input": prompt})
    output_text = result["output"]

    df = None
    try:
        # Case 1: If LLM returns an HTML or Markdown table
        if "<table" in output_text or output_text.strip().startswith("|"):
            df = pd.read_html(StringIO(output_text))[0]
        else:
            # Case 2: Try to parse "1. Product: $1234.56" format
            pattern = r"\d+\.\s*([A-Za-z0-9\s\-\_]+):?\s*\$?([\d,\.]+)"
            matches = re.findall(pattern, output_text)
            if matches:
                df = pd.DataFrame(matches, columns=["Entity", "Value"])
                df["Value"] = df["Value"].str.replace(',', '').astype(float)

    except Exception as e:
        st.error(f"Parsing failed: {e}")

    # If we have structured data
    if df is not None and not df.empty:
        st.write("### Final Query Result")
        st.dataframe(df)

        st.write("### Data Summary")
        st.dataframe(df.describe(include='all'))

        try:
            summary_prompt = f"Analyze this table and provide 3-4 key insights:\n\n{df.to_string(index=False)}"
            insights = llm.invoke(summary_prompt).content
            st.subheader("AI Analysis")
            st.write(insights)
        except Exception as e:
            st.error(f"AI Summary failed: {e}")

        if visualize:
            st.subheader("📊 Visualization")
            auto_visualize(df)

        return df

    # If no structured data was extracted
    st.write("### Final Output (unstructured)")
    st.write(output_text)
    return output_text
