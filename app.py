import streamlit as st
from pages.voters import show_voters
from pages.dashboard import show_dashboard

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Village Demographic Dashboard",
    page_icon="🗳️",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------

defaults = {
    "search_name": "", "gender": "All", "house_no": "", "polling_station": "",
    "min_age": 18, "max_age": 120, "search_clicked": False
    }

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# Navigation
# -----------------------------

pages = {
    "": [
        st.Page(show_voters, title="Voters", icon="👥"),
        st.Page(show_dashboard, title="Dashboard", icon="📊")
    ]
}

pg = st.navigation(pages)
pg.run()