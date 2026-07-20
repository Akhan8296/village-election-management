import streamlit as st
import pandas as pd
from services.voter_service import get_voters

st.set_page_config(
    page_title="Village Election Management",
    page_icon="🗳️",
    layout="wide"
)

st.title("🗳️ Village Election Management")

col1 , col2 = st.columns(2)
with col1:
    search_name = st.text_input("🔍 Search Voter Name")
with col2:
    gender = st.selectbox("Gender",[ "All", "Male", "Female"])

rows = get_voters(search_name)

columns = [
    "EPIC NO",
    "Booth",
    "Serial",
    "Polling Station",
    "Name",
    "Relation",
    "Relative Name",
    "House",
    "Age",
    "Gender"
]

df = pd.DataFrame(rows, columns=columns)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)