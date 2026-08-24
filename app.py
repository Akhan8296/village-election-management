import streamlit as st
from pages.voters import show_voters
from pages.dashboard import show_dashboard
from pages.update_voter import show_update_voter
from pages.login import show_login
from pages.user_management import show_user_management
from services.permission_service import has_permission
from pages.village_management import show_village_management
from services.village_service import get_villages
from pages.concern_management import show_concern_management

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

if has_permission("EDIT_VOTER"):
    nav_pages.insert(2, st.Page(show_update_voter, title="Update Voter", icon="✏️"))

if has_permission("MANAGE_USERS"):
    nav_pages.insert(3, st.Page(show_user_management, title="User Management", icon="👥"))

if st.session_state.get("role") == "POWER":
    nav_pages.insert(2, st.Page(show_village_management, title="Village Management", icon="🏘️"))

if st.session_state.get("role") in ["TEAM", "ADMIN", "POWER"]:
    nav_pages.append(
        st.Page(show_concern_management, title="Concerns", icon="⚠️")
    )
    
pages = {"": nav_pages}

pg = st.navigation(pages)

if st.session_state.get("is_logged_in"):
    sidebar_name = st.session_state.get("full_name") or st.session_state.get("username")
    sidebar_role = st.session_state.get("role", "").title()
    village_id = st.session_state.get("village_id")

    if sidebar_role == "Power":
        village_name = "All Villages"
    else:
        villages = get_villages()
        village_name = next((v[1] for v in villages if v[0] == village_id), "Unknown Village")

    st.sidebar.markdown(
        f"""
        <div style="position: fixed;bottom: 0;left: 0;width: 244px;padding: 12px 15px;border-top: 1px solid #ddd;">
            <div style="font-size: 13px;color:#777;">Logged in user</div>
            <div style="font-size: 15px;margin-top:5px;">👤 &nbsp;<b>{sidebar_name}</b></div>
            <div style="font-size: 13px;color:#777;margin-left:28px;">{sidebar_role} • {village_name}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.sidebar.markdown(
        """
        <div style="position: fixed;bottom: 0;left: 0;width: 244px;padding: 12px 15px;border-top: 1px solid #ddd;">
            <div style="font-size: 13px;color:#777;">Current access</div>
            <div style="font-size: 15px;margin-top:5px;">🌐 &nbsp;<b>Public User</b></div>
        </div>
        """,
        unsafe_allow_html=True
    )
pg.run()

