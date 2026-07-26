import streamlit as st
import pandas as pd
from services.voter_service import get_voters

st.set_page_config(
    page_title="Village Election Management",
    page_icon="🗳️",
    layout="wide"
)

st.markdown("""
<h1 style="    text-align:center;    background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;    font-weight:bold;    font-size: 4rem;">Village Election Management</h1>
""", unsafe_allow_html=True)

col1 , col2 = st.columns(2)
with col1:
    search_name = st.text_input("Voter Name")
with col2:
    gender = st.selectbox("Gender",[ "All", "Male", "Female"])

col3 , col4 = st.columns(2)
with col3:
    house_no = st.text_input("House No")
with col4:
    polling_station = st.text_input("Polling Station")

col5 , col6 ,col7 , col8 = st.columns(4)

with col5:
    min_age = st.number_input("Min Age", min_value=18, max_value=120, value=18)
with col6:
    max_age = st.number_input("Max Age", min_value=0, max_value=120, value=120)

col11 , col12 ,col13 ,col14 ,col15 ,col16 = st.columns(6)
with col15:
    search = st.button("Search" , use_container_width=True)
with col16:
    reset = st.button("Reset" , use_container_width=True)
if reset:
    st.write("Resetting the form...")
    st.session_state.search_name = ""
    st.session_state.gender = "All"
    st.session_state.house_no = ""
    st.session_state.polling_station = ""
    st.session_state.min_age = 18
    st.session_state.max_age = 120
    st.rerun()

if search:
    rows = get_voters(search_name=search_name,house_no=house_no,polling_station=polling_station, gender=gender,min_age=min_age,max_age=max_age)
    columns = ["EPIC NO","Booth","Serial","Polling Station","Name","Relation","Relative Name","House","Age","Gender"]
    df = pd.DataFrame(rows, columns=columns)
    st.dataframe(df,use_container_width=True,hide_index=True)
