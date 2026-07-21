from database import get_connection

def get_voters(search_name="",house_no="",gender="All",min_age=0,max_age=120,limit=100):
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
    # Add house number condition if provided
    if house_no:
        sql += """
            AND HOUSE_NO = :house_no
        """
        params["house_no"] = house_no

    # Add gender condition if not "All"
    if gender != "All":
        sql += """
            AND GENDER = :gender
        """
        params["gender"] = gender

    # Add age range conditions
    if min_age > 0:
        sql += """
            AND AGE >= :min_age
        """
        params["min_age"] = min_age

    if max_age < 120:
        sql += """
            AND AGE <= :max_age
        """
        params["max_age"] = max_age

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