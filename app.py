import streamlit as st
from pages.voters import show_voters
from pages.dashboard import show_dashboard

# Page Configuration
st.set_page_config(page_title="Village Demographic Dashboard",page_icon="🗳️",layout="wide")

st.markdown("""
<style>
[data-testid="stSidebarNav"]::before {
    content: "🗳️Village Demographic";
    display: block;
    font-size: 20px;
    font-weight: 600;
    text-align: center;
    padding: 10px 5px 15px 5px;
}
</style>
""", unsafe_allow_html=True)

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