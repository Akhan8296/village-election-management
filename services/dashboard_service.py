import pandas as pd
import streamlit as st
from database import get_connection

def get_village_filter(selected_village_id=None):
    role = st.session_state.get("role")
    village_id = st.session_state.get("village_id")

    # POWER can select a village or view all villages
    if role == "POWER":
        if selected_village_id is not None:
            return " WHERE VILLAGE_ID = :village_id ", {"village_id": selected_village_id}
        return "", {}

    # Logged-in users see only their village
    if st.session_state.get("is_logged_in"):
        return " WHERE VILLAGE_ID = :village_id ", {"village_id": village_id}

    # Public currently sees Korrahee
    return " WHERE VILLAGE_ID = :village_id ", {"village_id": 1}


def get_gender_data(selected_village_id=None):
    where_clause, params = get_village_filter(selected_village_id)

    query = f"""
        SELECT GENDER, COUNT(*) AS VOTER_COUNT
        FROM VOTERS
        {where_clause}
        GROUP BY GENDER
        ORDER BY GENDER
    """

    connection = get_connection()
    try:
        return pd.read_sql(query, connection, params=params)
    finally:
        connection.close()


def get_age_data(selected_village_id=None):
    where_clause, params = get_village_filter(selected_village_id)

    query = f"""
        SELECT
            CASE
                WHEN AGE BETWEEN 18 AND 25 THEN '18-25'
                WHEN AGE BETWEEN 26 AND 35 THEN '26-35'
                WHEN AGE BETWEEN 36 AND 45 THEN '36-45'
                WHEN AGE BETWEEN 46 AND 55 THEN '46-55'
                WHEN AGE >= 56 THEN '56+'
            END AS AGE_GROUP,
            COUNT(*) AS VOTER_COUNT
        FROM VOTERS
        {where_clause}
        GROUP BY
            CASE
                WHEN AGE BETWEEN 18 AND 25 THEN '18-25'
                WHEN AGE BETWEEN 26 AND 35 THEN '26-35'
                WHEN AGE BETWEEN 36 AND 45 THEN '36-45'
                WHEN AGE BETWEEN 46 AND 55 THEN '46-55'
                WHEN AGE >= 56 THEN '56+'
            END
        ORDER BY AGE_GROUP
    """

    connection = get_connection()
    try:
        return pd.read_sql(query, connection, params=params)
    finally:
        connection.close()


def get_house_data(selected_village_id=None):
    where_clause, params = get_village_filter(selected_village_id)

    query = f"""
        SELECT HOUSE_NO, COUNT(*) AS VOTER_COUNT
        FROM VOTERS
        {where_clause}
        GROUP BY HOUSE_NO
        ORDER BY HOUSE_NO
    """

    connection = get_connection()
    try:
        return pd.read_sql(query, connection, params=params)
    finally:
        connection.close()


def get_gender_age_data(selected_village_id=None):
    where_clause, params = get_village_filter(selected_village_id)
    query = f"""
        SELECT
            CASE
                WHEN AGE BETWEEN 18 AND 25 THEN '18-25'
                WHEN AGE BETWEEN 26 AND 35 THEN '26-35'
                WHEN AGE BETWEEN 36 AND 45 THEN '36-45'
                WHEN AGE BETWEEN 46 AND 55 THEN '46-55'
                WHEN AGE >= 56 THEN '56+'
            END AS AGE_GROUP,
            GENDER,
            COUNT(*) AS VOTER_COUNT
        FROM VOTERS
        {where_clause}
        GROUP BY
            CASE
                WHEN AGE BETWEEN 18 AND 25 THEN '18-25'
                WHEN AGE BETWEEN 26 AND 35 THEN '26-35'
                WHEN AGE BETWEEN 36 AND 45 THEN '36-45'
                WHEN AGE BETWEEN 46 AND 55 THEN '46-55'
                WHEN AGE >= 56 THEN '56+'
            END,
            GENDER
        ORDER BY AGE_GROUP, GENDER
    """

    connection = get_connection()
    try:
        return pd.read_sql(query, connection, params=params)
    finally:
        connection.close()


def get_kpi_data(selected_village_id=None):
    where_clause, params = get_village_filter(selected_village_id)

    query = f"""
        SELECT
            COUNT(*) AS TOTAL_VOTERS,
            NVL(SUM(CASE WHEN GENDER = 'Male' THEN 1 ELSE 0 END), 0) AS MALE_VOTERS,
            NVL(SUM(CASE WHEN GENDER = 'Female' THEN 1 ELSE 0 END), 0) AS FEMALE_VOTERS,
            COUNT(DISTINCT VILLAGE_ID || '-' || HOUSE_NO) AS TOTAL_HOUSES,
            NVL(ROUND(AVG(AGE), 1), 0) AS AVG_AGE
        FROM VOTERS
        {where_clause}
    """

    connection = get_connection()
    try:
        df = pd.read_sql(query, connection, params=params)
        return df.iloc[0]
    finally:
        connection.close()