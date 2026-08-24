import streamlit as st
import pandas as pd
from services.voter_service import get_voters
from services.village_service import get_villages
from services.concern_service import create_concern

def clear_filters():
    st.session_state.search_name = ""
    st.session_state.gender = "All"
    st.session_state.house_no = ""
    st.session_state.part_no = ""
    st.session_state.min_age = 18
    st.session_state.max_age = 120
    st.session_state.search_clicked = False

def show_voters(enable_concern=True):
    st.markdown("""
    <h2 style="font-size: 28px; margin-top: -25px; margin-bottom: 10px; font-weight: 600;">
        Search Voters
    </h2>
    """, unsafe_allow_html=True)

    selected_village_id = None

    if st.session_state.get("role") == "POWER":
        villages = get_villages()
        village_options = {"All Villages": None}
        village_options.update({v[1]: v[0] for v in villages if v[2] == "Y"})
        selected_village = st.selectbox("Village", list(village_options.keys()))
        selected_village_id = village_options[selected_village]

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.text_input("Voter Name", placeholder="Voter Name", key="search_name", label_visibility="collapsed")
    with col2:
        st.selectbox("Gender", ["All", "Male", "Female"], key="gender", label_visibility="collapsed")
    with col3:
        st.text_input("House No", placeholder="House No", key="house_no", label_visibility="collapsed")
    with col4:
        st.text_input("Part no", placeholder="Part no", key="part_no", label_visibility="collapsed")
    with col5:
        st.number_input("Min Age", min_value=18, max_value=120, value=18, key="min_age", label_visibility="collapsed")
    with col6:
        st.number_input("Max Age", min_value=18, max_value=120, value=120, key="max_age", label_visibility="collapsed")

    left, search_col, reset_col, right = st.columns([3, 1, 1, 3])

    with search_col:
        if st.button("Search", width="stretch"):
            st.session_state.search_clicked = True

    with reset_col:
        st.button("Reset", on_click=clear_filters, width="stretch")

    rows = []

    if st.session_state.search_clicked:
        rows = get_voters(
            search_name=st.session_state.search_name,
            house_no=st.session_state.house_no,
            part_no=st.session_state.part_no,
            gender=st.session_state.gender,
            min_age=st.session_state.min_age,
            max_age=st.session_state.max_age,
            selected_village_id=selected_village_id
        )

    columns = ["Serial no", "EPIC ID", "Name", "Relation", "Relative Name", "Age", "Gender", "House no", "booth_name", "Part no"]
    df = pd.DataFrame(rows, columns=columns)

    if st.session_state.search_clicked:
        st.success(f"Found {len(df)} voter(s).")
        st.dataframe(df, hide_index=True, width="stretch")

    # Concern Reporting
    if enable_concern and st.session_state.search_clicked and not df.empty:
        st.divider()
        st.subheader("⚠️ Report Incorrect Voter Data")

        if st.session_state.get("role") == "POWER" and selected_village_id is None:
            st.info("Select a specific village above before reporting incorrect data.")
        else:
            voter_options = {
                f"{row['Name']} - {row['EPIC ID']}": index
                for index, row in df.iterrows()
            }

            selected_voter_label = st.selectbox(
                "Select Voter",
                ["Select Voter"] + list(voter_options.keys()),
                key="concern_voter"
            )

            if selected_voter_label != "Select Voter":
                voter = df.loc[voter_options[selected_voter_label]]

                field_map = {
                    "EPIC ID": "EPIC_ID",
                    "Serial No": "SERIAL_NO",
                    "Name": "NAME",
                    "Relation": "REL_TYPE",
                    "Relative Name": "REL_NAME",
                    "Age": "AGE",
                    "Gender": "GENDER",
                    "House No": "HOUSE_NO",
                    "Booth Name": "BOOTH_NAME",
                    "Part No": "PART_NO"
                }

                selected_fields = st.multiselect(
                    "Which details are incorrect?",
                    list(field_map.keys())
                )

                if st.button("⚠️ Report Selected Fields as Incorrect", type="primary"):
                    if not selected_fields:
                        st.error("Please select at least one incorrect field.")
                    else:
                        value_map = {
                            "EPIC_ID": voter["EPIC ID"],
                            "SERIAL_NO": voter["Serial no"],
                            "NAME": voter["Name"],
                            "REL_TYPE": voter["Relation"],
                            "REL_NAME": voter["Relative Name"],
                            "AGE": voter["Age"],
                            "GENDER": voter["Gender"],
                            "HOUSE_NO": voter["House no"],
                            "BOOTH_NAME": voter["booth_name"],
                            "PART_NO": voter["Part no"]
                        }

                        incorrect_fields = {
                            field_map[field]: value_map[field_map[field]]
                            for field in selected_fields
                        }

                        if st.session_state.get("role") == "POWER":
                            concern_village_id = selected_village_id
                        elif st.session_state.get("is_logged_in"):
                            concern_village_id = st.session_state["village_id"]
                        else:
                            concern_village_id = 1  # Korrahee public access for now

                        try:
                            concern_id = create_concern(
                                epic_id=voter["EPIC ID"],
                                village_id=concern_village_id,
                                incorrect_fields=incorrect_fields,
                                raised_by_type="USER" if st.session_state.get("is_logged_in") else "PUBLIC",
                                raised_by_user_id=st.session_state.get("user_id")
                            )

                            st.success(f"✅ Concern #{concern_id} submitted successfully.")

                        except Exception as e:
                            st.error(f"❌ Concern submission failed: {e}")

    return df