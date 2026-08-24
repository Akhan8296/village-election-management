import streamlit as st
import pandas as pd
from services.voter_service import get_voters, update_voter
from pages.voters import show_voters
from services.permission_service import has_permission

def show_update_voter():
    # Admin protection
# Permission protection
    if not st.session_state.get("is_logged_in"):
        st.error("🔐 Login required.")
        st.stop()

    if not has_permission("EDIT_VOTER"):
        st.error("🚫 You don't have permission to edit voters.")
        st.stop()

    df = show_voters(enable_concern=False)

    st.markdown("### Select Voter")
    epic_options = df["EPIC ID"].tolist()
    col1, col2 ,right = st.columns([3, 2, 5])
    with col1:
        epic_options_with_placeholder = ["Select EPIC ID"] + epic_options
        selected_epic = st.selectbox(
            "Select EPIC ID",epic_options_with_placeholder,index=0,
            label_visibility="collapsed",key="selected_update_epic"
        )
    with col2:
        if st.button("Load Voter", width="stretch"):
            if selected_epic != "Select EPIC ID":
                selected_voter = df[df["EPIC ID"] == selected_epic].iloc[0]
                st.session_state.selected_voter = selected_voter
    if "selected_voter" in st.session_state:
        voter = st.session_state.selected_voter
        st.success(f"Voter selected: {voter['Name']}")
        st.markdown("### Edit Voter Details")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("EPIC ID",value=str(voter["EPIC ID"]), disabled=True)
            name = st.text_input("Name", value=str(voter["Name"]))
            relation_options = ["Father","Husband","Mother","Other"]
            rel_type = st.selectbox("Relation",relation_options,index=relation_options.index(voter["Relation"]))
            rel_name = st.text_input("Relative Name",value=str(voter["Relative Name"]))
            house_no = st.number_input("House No",min_value=0,max_value=9999,value=int(voter["House no"]))
        with col2:
            st.text_input("Serial No",value=str(voter["Serial no"]),disabled=True)
            age = st.number_input("Age",min_value=18,max_value=120,value=int(voter["Age"]))
            gender_options = ["Male","Female","Other"]
            gender = st.selectbox("Gender",gender_options,index=gender_options.index(voter["Gender"]))
            part_no = st.text_input("Part no",value=str(voter["Part no"]))
        st.markdown("---")
        if st.button("💾 Save Changes", type="primary", width="stretch"):       
            # Validation
            if not name.strip():
                st.error("Name cannot be empty.")       
            elif not rel_name.strip():
                st.error("Relative Name cannot be empty.")      
            elif not part_no.strip():
                st.error("Part no cannot be empty.")        
            else:
                try:
                    rows_updated = update_voter(
                        epic_id=voter["EPIC ID"],
                        name=name.strip(),
                        rel_type=rel_type,
                        rel_name=rel_name.strip(),
                        age=age,
                        gender=gender,
                        house_no=house_no,
                        part_no=part_no.strip()
                    )       
                    if rows_updated == 1:
                        st.success("✅ Voter details updated successfully.")        
                        # Remove selected voter so fresh data is loaded
                        del st.session_state.selected_voter     
                    else:
                        st.error("❌ Voter could not be updated.")      
                except Exception as e:
                    st.error(f"❌ Update failed: {e}")