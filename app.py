import streamlit as st
import pandas as pd
import markdown
from io import StringIO

# Set page title
st.set_page_config(page_title="Markdown Previewer", layout="wide")

# Apply custom styling for light and dark themes
st.markdown("""
    <style>
        html, body, [class*="st"]  {
            color: var(--text-color);
            background-color: var(--bg-color);
        }
        .stTextArea textarea {
            font-size: 16px;
            font-family: monospace;
            background-color: var(--input-bg);
            padding: 10px;
            color: var(--text-color);
        }
        .stMarkdown {
            border: 1px solid var(--border-color);
            padding: 15px;
            background-color: var(--content-bg);
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --text-color: #ffffff;
                --bg-color: #121212;
                --input-bg: #1e1e1e;
                --border-color: #333;
                --content-bg: #222;
            }
        }
        @media (prefers-color-scheme: light) {
            :root {
                --text-color: #000000;
                --bg-color: #ffffff;
                --input-bg: #f8f9fa;
                --border-color: #ddd;
                --content-bg: #ffffff;
            }
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