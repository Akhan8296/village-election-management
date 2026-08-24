import streamlit as st
from services.village_service import get_villages, create_village, update_village_status

def show_village_management():
    if st.session_state.get("role") != "POWER":
        st.error("🚫 Power access required.")
        st.stop()

    villages = get_villages()

    st.subheader("Existing Villages")
    if villages:
        village_data = [
            {
                "Village ID": v[0],
                "Village Name": v[1],
                "Status": "Active" if v[2] == "Y" else "Inactive"
            }
            for v in villages
        ]
        st.dataframe(village_data, hide_index=True, width="stretch")
    else:
        st.info("No villages found.")

    st.divider()
    st.subheader("Add Village")

    village_name = st.text_input("Village Name")

    if st.button("Add Village", type="primary"):
        if not village_name.strip():
            st.error("Village name is required.")
            return

        try:
            create_village(village_name)
            st.success(f"✅ Village '{village_name}' created successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Village creation failed: {e}")

    st.divider()
    st.subheader("Edit Village")

    if villages:
        village_map = {v[1]: v for v in villages}
        selected_name = st.selectbox("Select Village", list(village_map.keys()))
        selected_village = village_map[selected_name]

        village_id = selected_village[0]
        current_status = selected_village[2]

        is_active = st.checkbox("Active", value=current_status == "Y")

        if st.button("Update Village"):
            try:
                update_village_status(village_id, "Y" if is_active else "N")
                st.success("✅ Village status updated.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Update failed: {e}")