import streamlit as st
from database import get_connection

def get_voters(search_name="", house_no="", part_no="", gender="All", min_age=0, max_age=120, limit=1000, selected_village_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT serial_no, epic_id, name, rel_type, rel_name, age, gender,
               house_no, booth_name, part_no
        FROM VOTERS
        WHERE 1 = 1
    """

    params = {}

    # Village restriction
    role = st.session_state.get("role")
    village_id = st.session_state.get("village_id")

    if role == "POWER":
        if selected_village_id is not None:
            sql += " AND VILLAGE_ID = :village_id"
            params["village_id"] = selected_village_id

    elif st.session_state.get("is_logged_in"):
        sql += " AND VILLAGE_ID = :village_id"
        params["village_id"] = village_id

    else:
        # Public access - Korrahee for now
        sql += " AND VILLAGE_ID = :village_id"
        params["village_id"] = 1

    if search_name:
        sql += " AND UPPER(NAME) LIKE UPPER(:search_name)"
        params["search_name"] = f"%{search_name}%"

    if house_no:
        sql += " AND HOUSE_NO = :house_no"
        params["house_no"] = house_no

    if part_no:
        sql += " AND UPPER(BOOTH_NAME) LIKE UPPER(:part_no)"
        params["part_no"] = f"%{part_no}%"

    if gender != "All":
        sql += " AND GENDER = :gender"
        params["gender"] = gender

    if min_age > 0:
        sql += " AND AGE >= :min_age"
        params["min_age"] = min_age

    if max_age < 120:
        sql += " AND AGE <= :max_age"
        params["max_age"] = max_age

    sql += f" FETCH FIRST {limit} ROWS ONLY"

    cursor.execute(sql, params)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows


def update_voter(epic_id, name, rel_type, rel_name, age, gender, house_no, part_no):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE VOTERS
        SET NAME = :name,
            REL_TYPE = :rel_type,
            REL_NAME = :rel_name,
            AGE = :age,
            GENDER = :gender,
            HOUSE_NO = :house_no,
            PART_NO = :part_no
        WHERE EPIC_ID = :epic_id
    """

    params = {
        "epic_id": epic_id,
        "name": name,
        "rel_type": rel_type,
        "rel_name": rel_name,
        "age": age,
        "gender": gender,
        "house_no": house_no,
        "part_no": part_no
    }

    # Critical security restriction
    if st.session_state.get("role") != "POWER":
        sql += " AND VILLAGE_ID = :village_id"
        params["village_id"] = st.session_state.get("village_id")

    cursor.execute(sql, params)
    conn.commit()

    rows_updated = cursor.rowcount

    cursor.close()
    conn.close()
    return rows_updated