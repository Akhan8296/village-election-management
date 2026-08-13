from argon2 import PasswordHasher
from database import get_connection

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

def create_user(username, password, role="VIEWER"):
    password_hash = hash_password(password)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO USERS (USERNAME, PASSWORD_HASH, ROLE)
        VALUES (:username, :password_hash, :role)
        """,
        username=username,
        password_hash=password_hash,
        role=role
    )

    connection.commit()
    cursor.close()
    connection.close()

#Find user + check active + verify password
def authenticate_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT USER_ID, USERNAME, PASSWORD_HASH, ROLE
        FROM USERS
        WHERE USERNAME = :username
          AND IS_ACTIVE = 'Y'
        """,
        username=username
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:
        return None

    user_id, username, password_hash, role = user

    if verify_password(password, password_hash):
        return {
            "user_id": user_id,
            "username": username,
            "role": role
        }

    return None