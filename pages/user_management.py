import streamlit as st
from datetime import datetime, time
from services.permission_service import has_permission
from services.village_service import get_villages
from services.auth_service import create_user, get_users_by_village, get_all_users, get_user_permissions, update_user_access

def show_user_management():
    if not has_permission("MANAGE_USERS"):
        st.error("🚫 You don't have permission to manage users.")
        st.stop()

    if st.session_state.get("role") == "POWER":
        users = get_all_users()
    else:
        users = get_users_by_village(st.session_state["village_id"])
    role = st.session_state.get("role")

    # Existing Users
    st.subheader("Existing Users")

    if users:
        user_data = [
            {
                "Name": u[1],
                "Username": u[2],
                "Role": u[3],
                "Status": "Active" if u[4] == "Y" else "Inactive",
                "Access Start": u[5],
                "Access End": u[6]
            }
            for u in users
        ]

        st.dataframe(user_data, hide_index=True, width="stretch")
    else:
        st.info("No Team or Guest users found.")

    st.divider()

    # Create User
    st.subheader("Create User")

    full_name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    current_role = st.session_state.get("role")

    if current_role == "POWER":
        villages = [v for v in get_villages() if v[2] == "Y"]
        village_map = {v[1]: v[0] for v in villages}

        selected_village = st.selectbox("Village", list(village_map.keys()))
        target_village_id = village_map[selected_village]

        role = st.selectbox("Role", ["ADMIN", "TEAM", "GUEST"])

    else:
        target_village_id = st.session_state["village_id"]
        role = st.selectbox("Role", ["TEAM", "GUEST"])

    col1, col2 = st.columns(2)

    with col1:
        access_start = st.date_input("Access Start Date")

    with col2:
        no_expiry = st.checkbox("No Expiry", value=True)
        access_end = None if no_expiry else st.date_input("Access End Date")

    permissions = st.multiselect(
        "Permissions",
        [
            "EDIT_VOTER",
            "ADD_VOTER",
            "DELETE_VOTER",
            "IMPORT_DATA",
            "EXPORT_DATA",
            "VIEW_REPORTS"
        ]
    )

    if st.button("Create User", type="primary"):
        if not full_name.strip() or not username.strip() or not password:
            st.error("Full name, username and password are required.")
            return

        start_datetime = datetime.combine(access_start, time.min)
        end_datetime = None if no_expiry else datetime.combine(access_end, time.max)

        try:
            create_user(
                username=username.strip(),
                password=password,
                full_name=full_name.strip(),
                role=role,
                village_id=target_village_id,
                permissions=permissions,
                access_start=start_datetime,
                access_end=end_datetime
            )

            st.success(f"✅ User '{username}' created successfully.")
            st.rerun()

        except Exception as e:
            st.error(f"❌ User creation failed: {e}")

    st.divider()

    # Edit User
    st.subheader("Edit User")

    if users:
        user_map = {f"{u[1]} ({u[2]})": u for u in users}

        selected_label = st.selectbox(
            "Select User",
            list(user_map.keys())
        )

        selected_user = user_map[selected_label]

        selected_user_id = selected_user[0]
        current_status = selected_user[4]
        current_end = selected_user[6]

        current_permissions = get_user_permissions(selected_user_id)

        is_active = st.checkbox(
            "Active",
            value=current_status == "Y"
        )

        no_expiry_edit = st.checkbox(
            "No Expiry",
            value=current_end is None,
            key="edit_no_expiry"
        )

        if no_expiry_edit:
            new_access_end = None

        else:
            default_end = current_end.date() if current_end else datetime.now().date()

            new_access_end_date = st.date_input(
                "Access End Date",
                value=default_end,
                key="edit_access_end"
            )

            new_access_end = datetime.combine(
                new_access_end_date,
                time.max
            )

        all_permissions = [
            "EDIT_VOTER",
            "ADD_VOTER",
            "DELETE_VOTER",
            "IMPORT_DATA",
            "EXPORT_DATA",
            "VIEW_REPORTS"
        ]

        updated_permissions = st.multiselect(
            "Permissions",
            all_permissions,
            default=current_permissions,
            key="edit_permissions"
        )

        if st.button("Update User", type="primary"):
            try:
                update_user_access(
                    user_id=selected_user_id,
                    is_active="Y" if is_active else "N",
                    access_end=new_access_end,
                    permissions=updated_permissions
                )

                st.success("✅ User updated successfully.")
                st.rerun()

            except Exception as e:
                st.error(f"❌ User update failed: {e}")

    else:
        st.info("No users available to edit.")