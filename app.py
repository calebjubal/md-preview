import streamlit as st
from PIL import Image

st.title("🚀 Markdown Preview")
st.text("A place where you see preview ASAP!")

# Optional: Add a simple logo (replace 'logo.png' with your actual image file)
st.sidebar.image("https://www.streamlit.io/images/brand/streamlit-mark-color.svg", width=100)

# Markdown input section (left sidebar)
markdown_input = st.sidebar.text_area("Enter your Markdown here:", height=300)
if markdown_input:
    # Display the rendered Markdown output on the main page
    st.markdown(markdown_input, unsafe_allow_html=True)

# Custom CSS for styling the app
st.markdown(
    """
    <style>
    .css-1d391kg {
        padding: 2rem;
    }
    .css-1lc4wcr {
        margin-top: 20px;
    }
    .css-1r6o3s6 {
        font-size: 1.5em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)