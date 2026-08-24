import streamlit as st
from services.concern_service import (
    get_pending_concerns, get_concern_fields, submit_proposed_changes,
    get_pending_approvals, approve_concern, reject_concern,
    reject_concern_by_team
)

def show_concern_management():
    role = st.session_state.get("role")

    if role not in ["TEAM", "ADMIN", "POWER"]:
        st.error("🚫 You don't have access to Concern Management.")
        st.stop()

    st.title("⚠️ Concern Management")

    is_power = role == "POWER"
    village_id = st.session_state.get("village_id")

    # ---------------- PENDING CONCERNS ----------------
    concerns = get_pending_concerns(
        village_id=village_id,
        power=is_power
    )

    st.subheader("Pending Concerns")

    if not concerns:
        st.info("No pending concerns.")

    else:
        concern_map = {
            f"#{c[0]} - {c[2]} - {c[1]}": c
            for c in concerns
        }

        selected_label = st.selectbox(
            "Select Concern",
            list(concern_map.keys()),
            key="pending_concern_select"
        )

        concern = concern_map[selected_label]

        concern_id = concern[0]
        epic_id = concern[1]
        voter_name = concern[2]
        concern_village_id = concern[3]

        st.write(f"**Voter Name:** {voter_name}")
        st.write(f"**EPIC ID:** {epic_id}")
        st.write(f"**Raised By:** {concern[5]}")
        st.write(f"**Raised At:** {concern[6]}")

        fields = get_concern_fields(concern_id)

        st.divider()
        st.subheader("Propose Corrections")

        proposed_values = {}

        for field_name, old_value, proposed_value, final_value in fields:
            st.caption(f"Current {field_name}: {old_value}")

            proposed_values[field_name] = st.text_input(
                f"Correct {field_name}",
                value=proposed_value or "",
                key=f"propose_{concern_id}_{field_name}"
            )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Submit for Admin Approval", type="primary", width="stretch"):
                if any(not str(value).strip() for value in proposed_values.values()):
                    st.error("Please provide a proposed value for every flagged field.")
                else:
                    try:
                        submit_proposed_changes(
                            concern_id=concern_id,
                            proposed_values=proposed_values,
                            user_id=st.session_state["user_id"],
                            village_id=concern_village_id if is_power else village_id,
                            power=is_power
                        )
                        st.success("✅ Proposed corrections submitted for Admin approval.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Submission failed: {e}")

        with col2:
            if role == "TEAM":
                if st.button("❌ Reject Concern", width="stretch"):
                    st.session_state["show_team_rejection"] = True

        if role == "TEAM" and st.session_state.get("show_team_rejection"):
            team_rejection_reason = st.text_area(
                "Reason for rejection",
                placeholder="Explain why this concern is incorrect...",
                key=f"team_rejection_reason_{concern_id}"
            )

            if st.button("Confirm Rejection"):
                if not team_rejection_reason.strip():
                    st.error("Rejection reason is required.")
                else:
                    try:
                        reject_concern_by_team(
                            concern_id=concern_id,
                            reason=team_rejection_reason.strip(),
                            user_id=st.session_state["user_id"],
                            village_id=village_id
                        )

                        st.session_state["show_team_rejection"] = False
                        st.success("✅ Concern rejected.")
                        st.rerun()

                    except Exception as e:
                        st.error(f"❌ Rejection failed: {e}")

    # ---------------- APPROVAL SECTION ----------------
    if role in ["ADMIN", "POWER"]:
        st.divider()
        st.subheader("✅ Pending Approvals")

        approvals = get_pending_approvals(
            village_id=village_id,
            power=is_power
        )

        if not approvals:
            st.info("No pending approvals.")

        else:
            approval_map = {
                f"#{a[0]} - {a[2]} - {a[1]}": a
                for a in approvals
            }

            selected_approval = st.selectbox(
                "Select Approval",
                list(approval_map.keys()),
                key="approval_select"
            )

            approval = approval_map[selected_approval]

            concern_id = approval[0]
            epic_id = approval[1]
            voter_name = approval[2]
            concern_village_id = approval[3]

            st.write(f"**Voter Name:** {voter_name}")
            st.write(f"**EPIC ID:** {epic_id}")
            st.write(f"**Proposed By User ID:** {approval[5]}")
            st.write(f"**Proposed At:** {approval[6]}")

            fields = get_concern_fields(concern_id)

            st.markdown("#### Review Proposed Changes")

            final_values = {}

            for field_name, old_value, proposed_value, final_value in fields:
                st.write(f"**{field_name}**")
                st.caption(f"Current value: {old_value}")
                st.caption(f"Team proposed: {proposed_value}")

                if field_name == "EPIC_ID":
                    st.warning("EPIC ID changes require database correction.")
                    continue

                final_values[field_name] = st.text_input(
                    f"Final {field_name}",
                    value=final_value or proposed_value or "",
                    key=f"final_{concern_id}_{field_name}"
                )

            st.markdown("#### Decision")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Approve Changes", type="primary", width="stretch"):
                    if not final_values:
                        st.error("No app-editable fields available.")

                    elif any(not str(value).strip() for value in final_values.values()):
                        st.error("Final values cannot be empty.")

                    else:
                        try:
                            approve_concern(
                                concern_id=concern_id,
                                final_values=final_values,
                                approver_user_id=st.session_state["user_id"],
                                village_id=concern_village_id if is_power else village_id,
                                power=is_power
                            )

                            st.success("✅ Changes approved and voter record updated.")
                            st.rerun()

                        except Exception as e:
                            st.error(f"❌ Approval failed: {e}")

            with col2:
                if st.button("❌ Reject", width="stretch"):
                    st.session_state["show_rejection_reason"] = True

            if st.session_state.get("show_rejection_reason"):
                rejection_reason = st.text_area(
                    "Rejection Reason",
                    key=f"rejection_{concern_id}"
                )

                if st.button("Confirm Rejection"):
                    if not rejection_reason.strip():
                        st.error("Please enter a rejection reason.")

                    else:
                        try:
                            reject_concern(
                                concern_id=concern_id,
                                reason=rejection_reason.strip(),
                                rejected_by=st.session_state["user_id"],
                                village_id=concern_village_id if is_power else village_id,
                                power=is_power
                            )

                            st.session_state["show_rejection_reason"] = False
                            st.success("Concern rejected.")
                            st.rerun()

                        except Exception as e:
                            st.error(f"❌ Rejection failed: {e}")