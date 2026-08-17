from database import get_connection

def get_voters(search_name="",house_no="", part_no = "" ,gender="All",min_age=0,max_age=120,limit=500):
    # Create database connection
    conn = get_connection()
    cursor = conn.cursor()

    # Base SQL query
    sql = """
        SELECT serial_no,epic_no, name, rel_type, rel_name,  age, gender,house_no, section, station_id
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

    if part_no:
        sql += """
            AND UPPER(SECTION) LIKE UPPER(:part_no)
        """
        params["part_no"] = f"%{part_no}%"

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

def update_voter(epic_no,name,rel_type,rel_name,age,gender,house_no,part_no): #part_no = STATION_ID
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE VOTERS
        SET
            NAME = :name,
            REL_TYPE = :rel_type,
            REL_NAME = :rel_name,
            AGE = :age,
            GENDER = :gender,
            HOUSE_NO = :house_no,
            station_id = :part_no
        WHERE EPIC_NO = :epic_no
    """

    params = {
        "epic_no": epic_no,
        "name": name,
        "rel_type": rel_type,
        "rel_name": rel_name,
        "age": age,
        "gender": gender,
        "house_no": house_no,
        "part_no": part_no
    }

    cursor.execute(sql, params)
    conn.commit()
    rows_updated = cursor.rowcount
    cursor.close()
    conn.close()
    return rows_updated