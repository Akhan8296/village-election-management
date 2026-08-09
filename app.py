import streamlit as st
from pages.voters import show_voters
from pages.dashboard import show_dashboard

# Page Configuration
st.set_page_config(page_title="Village Demographic Dashboard",page_icon="🗳️",layout="wide")
st.sidebar.markdown(
    """
    <div style="text-align:center; padding:10px 0 15px 0;">
        <h2 style="margin:0;">🗳️ Election Management</h2>
        <p style="margin:4px 0 0 0; font-size:13px;">
            Village Election System
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Session State
defaults = {
    "search_name": "", "gender": "All", "house_no": "", "polling_station": "",
    "min_age": 18, "max_age": 120, "search_clicked": False
    }

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Navigation
pages = {
    "": [
        st.Page(show_dashboard, title="Dashboard", icon="📊"),
        st.Page(show_voters, title="Search Voters", icon="🔍"),
        st.Page("pages/update_voter.py", title="Update Voter", icon="✏️")
    ]
}

pg = st.navigation(pages)
pg.run()