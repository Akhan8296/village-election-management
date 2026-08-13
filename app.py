import streamlit as st
from pages.voters import show_voters
from pages.dashboard import show_dashboard
from services.auth_service import authenticate_user
from pages.update_voter import show_update_voter

# Page Configuration
st.set_page_config(page_title="Village Demographic Dashboard",page_icon="🗳️",layout="wide")

# Top-right Profile / Notification UI
# Top-right Profile / Notification UI
col1, col2, col3 = st.columns([16, 1, 1])

with col2:
    st.button("🔔", key="notifications")

with col3:
    with st.popover("👤", use_container_width=True):
        if st.session_state.get("is_logged_in", False):
            st.markdown(
                f"**{st.session_state['username']}**  \n"
                f"{st.session_state['role'].title()}"
            )

            st.divider()

            if st.button("🚪 Logout", use_container_width=True):
                st.session_state["is_logged_in"] = False
                st.session_state.pop("user_id", None)
                st.session_state.pop("username", None)
                st.session_state.pop("role", None)
                st.rerun()

        else:
            st.markdown("**Guest User**  \nPublic Access")

            st.divider()

            if st.button("🔐 Admin Login", use_container_width=True):
                st.session_state["show_admin_login"] = True

if st.session_state.get("show_admin_login", False):
    with st.container(border=True):
        st.subheader("🔐 Admin Login")

        username = st.text_input("Username", key="admin_username")
        password = st.text_input("Password", type="password", key="admin_password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login", type="primary", use_container_width=True):
                user = authenticate_user(username, password)

                if user and user["role"] == "ADMIN":
                    st.session_state["is_logged_in"] = True
                    st.session_state["user_id"] = user["user_id"]
                    st.session_state["username"] = user["username"]
                    st.session_state["role"] = user["role"]
                    st.session_state["show_admin_login"] = False
                    st.rerun()
                else:
                    st.error("Invalid administrator credentials.")

        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state["show_admin_login"] = False
                st.rerun()

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

