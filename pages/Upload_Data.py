import streamlit as st
import pandas as pd

st.title("📁 Upload Data")

file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if file:
    df = pd.read_csv(file)

    st.success("File Uploaded!")
    st.dataframe(df)