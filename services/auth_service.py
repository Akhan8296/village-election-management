from argon2 import PasswordHasher
from database import get_connection
from datetime import datetime


ph = PasswordHasher()

#Create/store password safely
def hash_password(password):
    return ph.hash(password)

#Check password against hash
def verify_password(password, password_hash):
    try:
        ph.verify(password_hash, password)
        return True
    except Exception:
        return False

def create_user(username, password, full_name, role, village_id, permissions, access_start=None, access_end=None):
    password_hash = hash_password(password)
    connection = get_connection()
    cursor = connection.cursor()

    try:
        user_id_var = cursor.var(int)

        cursor.execute("""
            INSERT INTO USERS (
                USERNAME, PASSWORD_HASH, FULL_NAME, ROLE, VILLAGE_ID,
                IS_ACTIVE, ACCESS_START_DATE, ACCESS_END_DATE
            )
            VALUES (
                :username, :password_hash, :full_name, :role, :village_id,
                'Y', :access_start, :access_end
            )
            RETURNING USER_ID INTO :user_id
        """, username=username, password_hash=password_hash, full_name=full_name,
            role=role, village_id=village_id, access_start=access_start,
            access_end=access_end, user_id=user_id_var)

        user_id = user_id_var.getvalue()[0]

        for permission in permissions:
            cursor.execute("""
                INSERT INTO USER_PERMISSIONS (USER_ID, PERMISSION_ID)
                SELECT :user_id, PERMISSION_ID
                FROM PERMISSIONS
                WHERE PERMISSION_NAME = :permission
            """, user_id=user_id, permission=permission)

        connection.commit()
        return user_id

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

#Find user + check active + verify password
def authenticate_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT USER_ID, USERNAME, PASSWORD_HASH, ROLE,
               FULL_NAME, VILLAGE_ID,
               ACCESS_START_DATE, ACCESS_END_DATE
        FROM USERS
        WHERE USERNAME = :username
          AND IS_ACTIVE = 'Y'
        """,
        username=username
    )

    user = cursor.fetchone()

    if not user:
        cursor.close()
        connection.close()
        return None

    (
        user_id, username, password_hash, role,
        full_name, village_id,
        access_start, access_end
    ) = user

    if not verify_password(password, password_hash):
        cursor.close()
        connection.close()
        return None

    # Check access period
    now = datetime.now()

    if access_start and now < access_start:
        cursor.close()
        connection.close()
        return None

    if access_end and now > access_end:
        cursor.close()
        connection.close()
        return None

    # Load permissions
    cursor.execute(
        """
        SELECT p.PERMISSION_NAME
        FROM USER_PERMISSIONS up
        JOIN PERMISSIONS p
          ON p.PERMISSION_ID = up.PERMISSION_ID
        WHERE up.USER_ID = :user_id
        """,
        user_id=user_id
    )

    permissions = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return {
        "user_id": user_id,
        "username": username,
        "full_name": full_name,
        "role": role,
        "village_id": village_id,
        "access_start": access_start,
        "access_end": access_end,
        "permissions": permissions
    }

def get_users_by_village(village_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT USER_ID, FULL_NAME, USERNAME, ROLE, IS_ACTIVE,
               ACCESS_START_DATE, ACCESS_END_DATE
        FROM USERS
        WHERE VILLAGE_ID = :village_id
          AND ROLE IN ('TEAM', 'GUEST')
        ORDER BY FULL_NAME
    """, village_id=village_id)

    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return users

def get_user_permissions(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT p.PERMISSION_NAME
        FROM USER_PERMISSIONS up
        JOIN PERMISSIONS p ON p.PERMISSION_ID = up.PERMISSION_ID
        WHERE up.USER_ID = :user_id
        ORDER BY p.PERMISSION_ID
    """, user_id=user_id)

    permissions = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return permissions

def update_user_access(user_id, is_active, access_end, permissions):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE USERS
            SET IS_ACTIVE = :is_active,
                ACCESS_END_DATE = :access_end
            WHERE USER_ID = :user_id
        """, is_active=is_active, access_end=access_end, user_id=user_id)

        cursor.execute(
            "DELETE FROM USER_PERMISSIONS WHERE USER_ID = :user_id",
            user_id=user_id
        )

        for permission in permissions:
            cursor.execute("""
                INSERT INTO USER_PERMISSIONS (USER_ID, PERMISSION_ID)
                SELECT :user_id, PERMISSION_ID
                FROM PERMISSIONS
                WHERE PERMISSION_NAME = :permission
            """, user_id=user_id, permission=permission)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

def get_all_users():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT USER_ID, FULL_NAME, USERNAME, ROLE, IS_ACTIVE,
               ACCESS_START_DATE, ACCESS_END_DATE, VILLAGE_ID
        FROM USERS
        WHERE ROLE IN ('ADMIN', 'TEAM', 'GUEST')
        ORDER BY VILLAGE_ID, FULL_NAME
    """)

    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users