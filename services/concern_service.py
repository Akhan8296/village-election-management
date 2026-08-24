from database import get_connection

def create_concern(epic_id, village_id, incorrect_fields, raised_by_type="PUBLIC", raised_by_user_id=None):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        concern_id_var = cursor.var(int)

        cursor.execute("""
            INSERT INTO VOTER_CONCERNS (
                EPIC_ID, VILLAGE_ID, STATUS,
                RAISED_BY_TYPE, RAISED_BY_USER_ID
            )
            VALUES (
                :epic_id, :village_id, 'PENDING',
                :raised_by_type, :raised_by_user_id
            )
            RETURNING CONCERN_ID INTO :concern_id
        """,
        epic_id=epic_id,
        village_id=village_id,
        raised_by_type=raised_by_type,
        raised_by_user_id=raised_by_user_id,
        concern_id=concern_id_var)

        concern_id = concern_id_var.getvalue()[0]

        for field_name, old_value in incorrect_fields.items():
            cursor.execute("""
                INSERT INTO VOTER_CONCERN_FIELDS (
                    CONCERN_ID, FIELD_NAME, OLD_VALUE
                )
                VALUES (
                    :concern_id, :field_name, :old_value
                )
            """,
            concern_id=concern_id,
            field_name=field_name,
            old_value=str(old_value) if old_value is not None else None)

        connection.commit()
        return concern_id

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

def get_pending_concerns(village_id=None, power=False):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        SELECT c.CONCERN_ID, c.EPIC_ID, v.NAME, c.VILLAGE_ID,
               c.STATUS, c.RAISED_BY_TYPE, c.RAISED_AT
        FROM VOTER_CONCERNS c
        JOIN VOTERS v
          ON v.EPIC_ID = c.EPIC_ID
         AND v.VILLAGE_ID = c.VILLAGE_ID
        WHERE c.STATUS = 'PENDING'
    """

    params = {}

    if not power:
        sql += " AND c.VILLAGE_ID = :village_id"
        params["village_id"] = village_id

    sql += " ORDER BY c.RAISED_AT"

    cursor.execute(sql, params)
    concerns = cursor.fetchall()
    cursor.close()
    connection.close()
    return concerns

def get_concern_fields(concern_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT FIELD_NAME, OLD_VALUE, PROPOSED_VALUE, FINAL_VALUE
        FROM VOTER_CONCERN_FIELDS
        WHERE CONCERN_ID = :concern_id
        ORDER BY FIELD_NAME
    """, concern_id=concern_id)

    fields = cursor.fetchall()
    cursor.close()
    connection.close()

    return fields

def submit_proposed_changes(concern_id, proposed_values, user_id, village_id, power=False):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Verify concern belongs to user's village and is still pending
        sql = """
            SELECT CONCERN_ID
            FROM VOTER_CONCERNS
            WHERE CONCERN_ID = :concern_id
              AND STATUS = 'PENDING'
        """

        params = {"concern_id": concern_id}

        if not power:
            sql += " AND VILLAGE_ID = :village_id"
            params["village_id"] = village_id

        cursor.execute(sql, params)

        if not cursor.fetchone():
            raise ValueError("Concern not found or access denied.")

        # Save Team's proposed values
        for field_name, proposed_value in proposed_values.items():
            cursor.execute("""
                UPDATE VOTER_CONCERN_FIELDS
                SET PROPOSED_VALUE = :proposed_value
                WHERE CONCERN_ID = :concern_id
                  AND FIELD_NAME = :field_name
            """,
            proposed_value=str(proposed_value).strip(),
            concern_id=concern_id,
            field_name=field_name)

        # Send to Admin approval
        cursor.execute("""
            UPDATE VOTER_CONCERNS
            SET STATUS = 'PENDING_APPROVAL',
                PROPOSED_BY = :user_id,
                PROPOSED_AT = SYSTIMESTAMP
            WHERE CONCERN_ID = :concern_id
        """, user_id=user_id, concern_id=concern_id)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

def get_pending_approvals(village_id=None, power=False):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        SELECT c.CONCERN_ID, c.EPIC_ID, v.NAME, c.VILLAGE_ID,
               c.STATUS, c.PROPOSED_BY, c.PROPOSED_AT
        FROM VOTER_CONCERNS c
        JOIN VOTERS v
          ON v.EPIC_ID = c.EPIC_ID
         AND v.VILLAGE_ID = c.VILLAGE_ID
        WHERE c.STATUS = 'PENDING_APPROVAL'
    """

    params = {}

    if not power:
        sql += " AND c.VILLAGE_ID = :village_id"
        params["village_id"] = village_id

    sql += " ORDER BY c.PROPOSED_AT"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def approve_concern(concern_id, final_values, approver_user_id, village_id=None, power=False):
    connection = get_connection()
    cursor = connection.cursor()

    allowed_fields = {
        "SERIAL_NO", "PART_NO", "BOOTH_NAME", "NAME", "REL_TYPE",
        "REL_NAME", "AGE", "GENDER", "HOUSE_NO"
    }

    try:
        sql = """
            SELECT EPIC_ID, VILLAGE_ID
            FROM VOTER_CONCERNS
            WHERE CONCERN_ID = :concern_id
              AND STATUS = 'PENDING_APPROVAL'
        """
        params = {"concern_id": concern_id}

        if not power:
            sql += " AND VILLAGE_ID = :village_id"
            params["village_id"] = village_id

        cursor.execute(sql, params)
        concern = cursor.fetchone()

        if not concern:
            raise ValueError("Concern not found or access denied.")

        epic_id, concern_village_id = concern

        for field_name, final_value in final_values.items():
            if field_name not in allowed_fields:
                raise ValueError(f"{field_name} cannot be updated through the app.")

            cursor.execute("""
                UPDATE VOTER_CONCERN_FIELDS
                SET FINAL_VALUE = :final_value
                WHERE CONCERN_ID = :concern_id
                  AND FIELD_NAME = :field_name
            """, final_value=str(final_value).strip(), concern_id=concern_id, field_name=field_name)

            # Field name is validated against the whitelist above.
            update_sql = f"""
                UPDATE VOTERS
                SET {field_name} = :final_value
                WHERE EPIC_ID = :epic_id
                  AND VILLAGE_ID = :village_id
            """

            cursor.execute(
                update_sql,
                final_value=final_value,
                epic_id=epic_id,
                village_id=concern_village_id
            )

        cursor.execute("""
            UPDATE VOTER_CONCERNS
            SET STATUS = 'APPROVED',
                APPROVED_BY = :approved_by,
                APPROVED_AT = SYSTIMESTAMP
            WHERE CONCERN_ID = :concern_id
        """, approved_by=approver_user_id, concern_id=concern_id)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

def reject_concern(concern_id, reason, rejected_by, village_id=None, power=False):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        sql = """
            UPDATE VOTER_CONCERNS
            SET STATUS = 'REJECTED',
                REJECTED_BY = :rejected_by,
                REJECTED_AT = SYSTIMESTAMP,
                REJECTION_REASON = :reason
            WHERE CONCERN_ID = :concern_id
              AND STATUS = 'PENDING_APPROVAL'
        """

        params = {
            "concern_id": concern_id,
            "rejected_by": rejected_by,
            "reason": reason
        }

        if not power:
            sql += " AND VILLAGE_ID = :village_id"
            params["village_id"] = village_id

        cursor.execute(sql, params)

        if cursor.rowcount != 1:
            raise ValueError("Concern not found or access denied.")

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

def get_notification_count(role, village_id=None):
    connection = get_connection()
    cursor = connection.cursor()

    if role == "TEAM":
        cursor.execute("""
            SELECT COUNT(*)
            FROM VOTER_CONCERNS
            WHERE VILLAGE_ID = :village_id
              AND STATUS = 'PENDING'
        """, village_id=village_id)

    elif role == "ADMIN":
        cursor.execute("""
            SELECT COUNT(*)
            FROM VOTER_CONCERNS
            WHERE VILLAGE_ID = :village_id
              AND STATUS = 'PENDING_APPROVAL'
        """, village_id=village_id)

    elif role == "POWER":
        cursor.execute("""
            SELECT COUNT(*)
            FROM VOTER_CONCERNS
            WHERE STATUS IN ('PENDING', 'PENDING_APPROVAL')
        """)

    else:
        cursor.close()
        connection.close()
        return 0

    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count

def reject_concern_by_team(concern_id, reason, user_id, village_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE VOTER_CONCERNS
            SET STATUS = 'REJECTED_BY_TEAM',
                TEAM_REJECTED_BY = :user_id,
                TEAM_REJECTED_AT = SYSTIMESTAMP,
                TEAM_REJECTION_REASON = :reason
            WHERE CONCERN_ID = :concern_id
              AND VILLAGE_ID = :village_id
              AND STATUS = 'PENDING'
        """,
        user_id=user_id,
        reason=reason,
        concern_id=concern_id,
        village_id=village_id)

        if cursor.rowcount != 1:
            raise ValueError("Concern not found, already processed, or access denied.")

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

def get_notification_summary(role, village_id=None):
    connection = get_connection()
    cursor = connection.cursor()

    if role == "TEAM":
        cursor.execute("""
            SELECT
                SUM(CASE WHEN STATUS = 'PENDING' THEN 1 ELSE 0 END)
            FROM VOTER_CONCERNS
            WHERE VILLAGE_ID = :village_id
        """, village_id=village_id)

        pending = cursor.fetchone()[0] or 0
        result = {"pending": pending, "approvals": 0}

    elif role == "ADMIN":
        cursor.execute("""
            SELECT
                SUM(CASE WHEN STATUS = 'PENDING_APPROVAL' THEN 1 ELSE 0 END)
            FROM VOTER_CONCERNS
            WHERE VILLAGE_ID = :village_id
        """, village_id=village_id)

        approvals = cursor.fetchone()[0] or 0
        result = {"pending": 0, "approvals": approvals}

    elif role == "POWER":
        cursor.execute("""
            SELECT
                SUM(CASE WHEN STATUS = 'PENDING' THEN 1 ELSE 0 END),
                SUM(CASE WHEN STATUS = 'PENDING_APPROVAL' THEN 1 ELSE 0 END)
            FROM VOTER_CONCERNS
        """)

        row = cursor.fetchone()
        result = {
            "pending": row[0] or 0,
            "approvals": row[1] or 0
        }

    else:
        result = {"pending": 0, "approvals": 0}

    cursor.close()
    connection.close()
    return result