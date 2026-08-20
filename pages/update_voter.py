import streamlit as st
import pandas as pd
from services.voter_service import get_voters, update_voter

def clear_update_filters():
    st.session_state.update_search_name = ""
    st.session_state.update_gender = "All"
    st.session_state.update_house_no = ""
    st.session_state.update_part_no = ""
    st.session_state.update_min_age = 18
    st.session_state.update_max_age = 120
    st.session_state.update_search_clicked = False

def show_update_voter():
    # Admin protection
    if st.session_state.get("role") != "ADMIN":
        st.error("🚫 Administrator access required.")
        st.stop()

    st.write("Search for a voter whose details you want to update:")

    # Search filters
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.text_input("Voter Name", placeholder="Voter Name",key="update_search_name",label_visibility="collapsed")

    with col2:
        st.selectbox("Gender",["All", "Male", "Female"],key="update_gender",label_visibility="collapsed")

    with col3:
        st.text_input("House No",placeholder="House No",key="update_house_no",label_visibility="collapsed")

    with col4:
        st.text_input("Part no",placeholder="Part no",key="update_part_no",label_visibility="collapsed")

    with col5:
        st.number_input("Min Age",min_value=18,max_value=120,value=18,key="update_min_age",label_visibility="collapsed")

    with col6:
        st.number_input("Max Age",min_value=18,max_value=120,value=120,key="update_max_age",label_visibility="collapsed")

    # Buttons
    left, search_col, reset_col, right = st.columns([3, 1, 1, 3])

    with search_col:
        if st.button("Search", width="stretch"):
            st.session_state.update_search_clicked = True

    with reset_col:
        st.button("Reset",on_click=clear_update_filters,width="stretch")

    # Search Results
    if st.session_state.get("update_search_clicked", False):
        rows = get_voters(
            search_name=st.session_state.update_search_name,
            house_no=st.session_state.update_house_no,
            part_no=st.session_state.update_part_no,
            gender=st.session_state.update_gender,
            min_age=st.session_state.update_min_age,
            max_age=st.session_state.update_max_age
        )

        columns = ["Serial","EPIC NO","Name","Relation","Relative Name","Age","Gender","House","Section","Part no"]

        df = pd.DataFrame(rows, columns=columns)
        st.success(f"Found {len(df)} voter(s).")
        st.dataframe(df,hide_index=True,width="stretch")

        st.markdown("### Select Voter")
        epic_options = df["EPIC NO"].tolist()

        col1, col2 ,right = st.columns([3, 2, 5])
        with col1:
            epic_options_with_placeholder = ["Select EPIC No"] + epic_options

            selected_epic = st.selectbox(
                "Select EPIC No",epic_options_with_placeholder,index=0,
                label_visibility="collapsed",key="selected_update_epic"
            )

        with col2:
            if st.button("Load Voter", width="stretch"):
                if selected_epic != "Select EPIC No":
                    selected_voter = df[df["EPIC NO"] == selected_epic].iloc[0]
                    st.session_state.selected_voter = selected_voter

        if "selected_voter" in st.session_state:
            voter = st.session_state.selected_voter
            st.success(f"Voter selected: {voter['Name']}")
            st.markdown("### Edit Voter Details")

            col1, col2 = st.columns(2)
            with col1:
                st.text_input("EPIC No",value=str(voter["EPIC NO"]), disabled=True)
                name = st.text_input("Name", value=str(voter["Name"]))
                relation_options = ["Father","Husband","Mother","Other"]
                rel_type = st.selectbox("Relation",relation_options,index=relation_options.index(voter["Relation"]))
                rel_name = st.text_input("Relative Name",value=str(voter["Relative Name"]))
                house_no = st.number_input("House No",min_value=0,max_value=9999,value=int(voter["House"]))
            with col2:
                st.text_input("Serial No",value=str(voter["Serial"]),disabled=True)
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
                    st.error("Section cannot be empty.")        
                else:
                    try:
                        rows_updated = update_voter(
                            epic_no=voter["EPIC NO"],
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