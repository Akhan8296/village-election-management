import streamlit as st
from services.auth_service import authenticate_user

def show_login():
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
                if st.button("🚪Logout", use_container_width=True):
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