import streamlit as st

def has_permission(permission):
    if st.session_state.get("role") == "POWER":
        return True
    return permission in st.session_state.get("permissions", [])