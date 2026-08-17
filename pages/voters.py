import streamlit as st
import pandas as pd
from services.voter_service import get_voters

def clear_filters():
    st.session_state.search_name = ""
    st.session_state.gender = "All"
    st.session_state.house_no = ""
    st.session_state.polling_station = ""
    st.session_state.min_age = 18
    st.session_state.max_age = 120
    st.session_state.search_clicked = False

def show_voters():
    st.markdown("""
    <h2 style="
        font-size: 28px;
        margin-top: -25px;
        margin-bottom: 10px;
        font-weight: 600;
    ">
        Search Voters
    </h2>
    """, unsafe_allow_html=True)

    # Search Filters
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.text_input("Voter Name",placeholder="Voter Name",key="search_name",label_visibility="collapsed")

    with col2:
        st.selectbox("Gender",["All", "Male", "Female"],key="gender",label_visibility="collapsed")

    with col3:
        st.text_input("House No",placeholder="House No",key="house_no",label_visibility="collapsed")

    with col4:
        st.text_input("Polling Station",placeholder="Polling Station",key="polling_station",label_visibility="collapsed")

    with col5:
        st.number_input("Min Age", min_value=18,max_value=120,value=18,key="min_age",label_visibility="collapsed")

    with col6:
        st.number_input("Max Age",min_value=18,max_value=120,value=120,key="max_age",label_visibility="collapsed")

    # Buttons
    left, search_col, reset_col, right = st.columns([3, 1, 1, 3])

    with search_col:
        if st.button("Search", width="stretch"):
            st.session_state.search_clicked = True

    with reset_col:
        st.button("Reset", on_click=clear_filters, width="stretch")

    # Search Results
    if st.session_state.search_clicked:
        rows = get_voters(
            search_name=st.session_state.search_name,
            house_no=st.session_state.house_no,
            polling_station=st.session_state.polling_station,
            gender=st.session_state.gender,
            min_age=st.session_state.min_age,
            max_age=st.session_state.max_age
        )
        #columns = ["EPIC NO", "Booth", "Serial", "Polling Station", "Name", "Relation", "Relative Name", "Age", "Gender", "House"]
        columns = ["Serial","EPIC NO", "Name", "Relation", "Relative Name", "Age", "Gender", "House","Booth","Polling Station"]
        df = pd.DataFrame(rows, columns=columns)
        
        st.success(f"Found {len(df)} voter(s).")
        st.dataframe(df, hide_index=True, width='stretch')
    