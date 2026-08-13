import streamlit as st
from pages.voters import show_voters
from pages.dashboard import show_dashboard

# Page Configuration
st.set_page_config(page_title="Village Demographic Dashboard",page_icon="🗳️",layout="wide")

import streamlit as st

# Top-right Profile / Notification UI
col1, col2, col3 = st.columns([16, 1, 1])

with col2:
    st.button("🔔", key="notifications")

with col3:
    if st.button("👤", key="profile"):
        st.session_state["show_profile"] = not st.session_state.get("show_profile", False)

if st.session_state.get("show_profile", False):
    st.markdown("""
    <div style="position:absolute; right:20px; top:10px; width:180px; padding:15px; background:white; border:1px solid #ddd;
        border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.15);z-index:999;">
        <b>Admin</b><br>
        <small>Administrator</small>
        <hr>
        Profile<br>
        Account Settings<br>
        Logout
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stSidebarNav"]::before {
    content: "🗳️Village Demographic";
    display: block;
    font-size: 20px;
    font-weight: 600;
    text-align: left;
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
        st.Page("pages/update_voter.py", title="Update Voter", icon="✏️"),
        st.Page("pages/settings.py", title="Settings", icon="⚙️")
    ]
}
pg = st.navigation(pages)

st.sidebar.markdown(
    """
    <div style="
        position: fixed;
        bottom: 0;
        left: 0;
        width: 244px;
        padding: 12px 15px;
        border-top: 1px solid #ddd;
    ">
        <div style="font-size: 13px; color: #555;">
            Logged in user
        </div>
        <div style="font-size: 15px; margin-top: 6px;">
            👤 &nbsp; Admin
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
pg.run()

