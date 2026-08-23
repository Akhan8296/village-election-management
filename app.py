import streamlit as st
from pages.voters import show_voters
from pages.dashboard import show_dashboard
from pages.update_voter import show_update_voter
from pages.login import show_login

# Page Configuration
st.set_page_config(page_title="Village Demographic Dashboard",page_icon="🗳️",layout="wide")

show_login();

# Session State
defaults = {
    "search_name": "", "gender": "All", "house_no": "", "polling_station": "",
    "min_age": 18, "max_age": 120, "search_clicked": False
    }

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.markdown("""
<style>
[data-testid="stSidebarNav"]::before {
    content: "🗳️Village Demographic"; 
    display: block; font-size: 20px; font-weight: 600; text-align: left; padding: 10px 5px 15px 5px;
}
</style>
""", unsafe_allow_html=True)

# Navigation
nav_pages = [
    st.Page(show_dashboard, title="Dashboard", icon="📊"),
    st.Page(show_voters, title="Search Voters", icon="🔍"),
    st.Page("pages/settings.py", title="Settings", icon="⚙️")
]

if st.session_state.get("role") == "ADMIN":
    nav_pages.insert(2, st.Page(show_update_voter, title="Update Voter", icon="✏️"))

pages = {"": nav_pages}

pg = st.navigation(pages)

st.sidebar.markdown(
    """
    <div style="position: fixed;bottom: 0;left: 0;width: 244px;padding: 12px 15px;border-top: 1px solid #ddd;">
        <div style="font-size: 13px; color: #555;">Logged in user</div>
        <div style="font-size: 15px; margin-top: 6px;">👤 &nbsp; Admin</div>
    </div>
    """,
    unsafe_allow_html=True
)
pg.run()

