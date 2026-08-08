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