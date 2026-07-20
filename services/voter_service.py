from database import get_connection

def get_voters(search_name="", limit=50):

    # Create database connection
    conn = get_connection()
    cursor = conn.cursor()

    # Base SQL query
    sql = """
        SELECT *
        FROM VOTERS
        WHERE 1 = 1
    """

    # Dictionary to hold bind variables
    params = {}

    # Add search condition if user entered a name
    if search_name:
        sql += """
            AND UPPER(NAME) LIKE UPPER(:search_name)
        """
        params["search_name"] = f"%{search_name}%"

    # Add row limit
    sql += f"""
        FETCH FIRST {limit} ROWS ONLY
    """

    # Execute query
    cursor.execute(sql, params)

    # Fetch data
    rows = cursor.fetchall()

    # Close connection
    cursor.close()
    conn.close()

    return rows