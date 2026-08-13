import streamlit as st

def show_update_voter():
    if st.session_state.get("role") != "ADMIN":
        st.error("🚫 Administrator access required.")
        st.stop()

    st.title("✏️ Update Voter")
    st.write("This page is available only to administrators.")