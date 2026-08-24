import streamlit as st
from services.auth_service import authenticate_user
from services.concern_service import get_notification_count
from services.concern_service import get_notification_summary

from services.auth_service import authenticate_user

def show_login():
    col1, col2, col3 = st.columns([16, 1, 1])

    with col2:
        role = st.session_state.get("role")
        village_id = st.session_state.get("village_id")

        summary = get_notification_summary(role, village_id)
        total = summary["pending"] + summary["approvals"]

        with st.popover(f"🔔 {total}" if total else "🔔"):
            if role == "TEAM":
                st.write(f"⚠️ Pending concerns: **{summary['pending']}**")

            elif role == "ADMIN":
                st.write(f"✅ Pending approvals: **{summary['approvals']}**")

            elif role == "POWER":
                st.write(f"⚠️ Pending concerns: **{summary['pending']}**")
                st.write(f"✅ Pending approvals: **{summary['approvals']}**")

            else:
                st.write("No notifications.")
    with col3:
        with st.popover("👤", use_container_width=True):
            if st.session_state.get("is_logged_in", False):
                st.markdown(
                    f"**{st.session_state.get('full_name', st.session_state['username'])}**  \n"
                    f"{st.session_state['role'].title()}"
                )
                st.divider()

                if st.button("🚪 Logout", use_container_width=True):
                    for key in ["user_id", "username", "full_name", "role", "village_id", "permissions"]:
                        st.session_state.pop(key, None)

                    st.session_state["is_logged_in"] = False
                    st.rerun()

            else:
                st.markdown("**Public User**  \nPublic Access")
                st.divider()

                if st.button("🔐 Login", use_container_width=True):
                    st.session_state["show_login_form"] = True

    if st.session_state.get("show_login_form", False):
        with st.container(border=True):
            st.subheader("🔐 Login")

            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Login", type="primary", use_container_width=True):
                    user = authenticate_user(username, password)

                    if user:
                        st.session_state["is_logged_in"] = True
                        st.session_state["user_id"] = user["user_id"]
                        st.session_state["username"] = user["username"]
                        st.session_state["full_name"] = user["full_name"]
                        st.session_state["role"] = user["role"]
                        st.session_state["village_id"] = user["village_id"]
                        st.session_state["permissions"] = user["permissions"]
                        st.session_state["show_login_form"] = False
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

            with col2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state["show_login_form"] = False
                    st.rerun()

