import streamlit as st
import pandas as pd
from io import StringIO

# Set page title
st.set_page_config(page_title="Markdown Previewer", layout="wide")

# Apply custom styling
st.markdown("""
    <style>
        .stTextArea textarea {
            font-size: 16px;
            font-family: monospace;
            background-color: #f8f9fa;
            padding: 10px;
        }
        .stMarkdown {
            border: 1px solid #ddd;
            padding: 15px;
            background-color: #ffffff;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# App title with styling
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📝 Live Markdown Preview</h1>", unsafe_allow_html=True)

# Sidebar for Markdown Input
st.sidebar.subheader("✍️ Markdown Input")
markdown_input = st.sidebar.text_area("Enter Markdown text:", "# Hello, Streamlit!\n\nThis is a **Markdown previewer**.")

# Extract tables and convert them into DataFrames
def extract_table(md_text):
    tables = []
    lines = md_text.split("\n")
    table_lines = []
    is_table = False
    
    for line in lines:
        if "|" in line:
            is_table = True
            table_lines.append(line)
        elif is_table:
            break
    
    if table_lines:
        table_str = "\n".join(table_lines)
        table_str = table_str.replace("—", "-")  # Fix broken formatting
        df = pd.read_csv(StringIO(table_str), delimiter="|", skipinitialspace=True)
        df = df.iloc[:, 1:-1]  # Remove extra empty columns
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
        tables.append(df)
    
    return tables

extracted_tables = extract_table(markdown_input)

# Main preview area
st.subheader("📄 Preview")
st.markdown(f"<div class='stMarkdown'>{markdown_input}</div>", unsafe_allow_html=True)

if extracted_tables:
    st.subheader("📊 Extracted Tables")
    for i, table in enumerate(extracted_tables):
        st.write(f"Table {i+1}:")
        st.dataframe(table)
