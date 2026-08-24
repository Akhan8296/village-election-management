from database import get_connection

def get_villages():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT VILLAGE_ID, VILLAGE_NAME, IS_ACTIVE
        FROM VILLAGES
        ORDER BY VILLAGE_NAME
    """)

    villages = cursor.fetchall()
    cursor.close()
    connection.close()
    return villages


def create_village(village_name):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO VILLAGES (VILLAGE_NAME, IS_ACTIVE)
            VALUES (:village_name, 'Y')
        """, village_name=village_name.strip())

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

def update_village_status(village_id, is_active):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE VILLAGES
            SET IS_ACTIVE = :is_active
            WHERE VILLAGE_ID = :village_id
        """, is_active=is_active, village_id=village_id)

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()