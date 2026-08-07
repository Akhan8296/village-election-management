import streamlit as st
import pandas as pd
from services.voter_service import get_voters

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Village Demographic Dashboard",
    page_icon="🗳️",
    layout="wide"
)

# -----------------------------
# Session State Initialization
# -----------------------------
defaults = {
    "search_name": "",
    "gender": "All",
    "house_no": "",
    "polling_station": "",
    "min_age": 18,
    "max_age": 120,
    "search_clicked": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# Reset Function
# -----------------------------
def clear_filters():
    st.session_state.search_name = ""
    st.session_state.gender = "All"
    st.session_state.house_no = ""
    st.session_state.polling_station = ""
    st.session_state.min_age = 18
    st.session_state.max_age = 120
    st.session_state.search_clicked = False


# -----------------------------
# Title
# -----------------------------
st.markdown("""
<div style="
    text-align:center;
    padding:20px;
    border-radius:15px;
    background:linear-gradient(135deg,#fff7e6,#ffffff,#e8f5e9);
    box-shadow:0 4px 12px rgba(0,0,0,0.2);
    margin-bottom:20px;
">
    <h1 style="
        margin:0;
        font-size:52px;
        font-weight:800;
        background:linear-gradient(90deg,#FF9933,#138808);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        letter-spacing:2px;
    ">
        🗳️ Village Demographic Dashboard
    </h1>
    <p style="
        color:#555;
        font-size:18px;
        margin-top:8px;
        font-style:italic;
    ">
        Village Insights • Population • Analytics
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Search Filters
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.text_input(
        "Voter Name",
        key="search_name"
    )

with col2:
    st.selectbox(
        "Gender",
        ["All", "Male", "Female"],
        key="gender"
    )

col3, col4 = st.columns(2)

with col3:
    st.text_input(
        "House No",
        key="house_no"
    )

with col4:
    st.text_input(
        "Polling Station",
        key="polling_station"
    )

col5, col6 = st.columns(2)

with col5:
    st.number_input(
        "Min Age",
        min_value=18,
        max_value=120,
        key="min_age"
    )

with col6:
    st.number_input(
        "Max Age",
        min_value=18,
        max_value=120,
        key="max_age"
    )

# -----------------------------
# Buttons
# -----------------------------

left, search_col, reset_col, right = st.columns([3, 1, 1, 3])

with search_col:
    if st.button("Search", use_container_width=True):
        st.session_state.search_clicked = True

with reset_col:
    st.button(
        "Reset",
        on_click=clear_filters,
        use_container_width=True
    )

# -----------------------------
# Search Results
# -----------------------------

if st.session_state.search_clicked:

    rows = get_voters(
        search_name=st.session_state.search_name,
        house_no=st.session_state.house_no,
        polling_station=st.session_state.polling_station,
        gender=st.session_state.gender,
        min_age=st.session_state.min_age,
        max_age=st.session_state.max_age
    )

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

    st.success(f"Found {len(df)} voter(s).")

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )