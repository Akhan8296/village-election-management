import pandas as pd
from database import get_connection

def get_gender_data():
    query = """ SELECT GENDER, COUNT(*) AS VOTER_COUNT FROM VOTERS GROUP BY GENDER ORDER BY GENDER """
    connection = get_connection()
    try:
        df = pd.read_sql(query, connection)
        return df
    finally:
        connection.close()

def get_age_data():
    query = """
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
        df = pd.read_sql(query, connection)
        return df
    finally:
        connection.close()

def get_house_data():
    query = """ SELECT HOUSE_NO, COUNT(*) AS VOTER_COUNT FROM VOTERS GROUP BY HOUSE_NO ORDER BY HOUSE_NO """
    connection = get_connection()
    try:
        df = pd.read_sql(query, connection)
        return df
    finally:
        connection.close()

def get_gender_age_data():
    query = """
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
        df = pd.read_sql(query, connection)
        return df
    finally:
        connection.close()

def get_kpi_data():
    query = """
        SELECT
            COUNT(*) AS TOTAL_VOTERS,
            SUM(CASE WHEN GENDER = 'Male' THEN 1 ELSE 0 END) AS MALE_VOTERS,
            SUM(CASE WHEN GENDER = 'Female' THEN 1 ELSE 0 END) AS FEMALE_VOTERS,
            COUNT(DISTINCT HOUSE_NO) AS TOTAL_HOUSES
        FROM VOTERS
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df.iloc[0]
    finally:
        connection.close()