import streamlit as st
from services.auth_service import authenticate_user

def show_login():
    st.markdown(
        """
        <div style="text-align:center; margin-top:80px;">
            <div style="font-size:48px;">🗳️</div>
            <h1>Village Election Management</h1>
            <p>Voter Management System</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", type="primary", use_container_width=True):
            user = authenticate_user(username, password)

            if user:
                st.session_state["is_logged_in"] = True
                st.session_state["user_id"] = user["user_id"]
                st.session_state["username"] = user["username"]
                st.session_state["role"] = user["role"]
                st.rerun()
            else:
                st.error("Invalid username or password.")