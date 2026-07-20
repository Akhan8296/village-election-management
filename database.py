import oracledb
from config import *

def get_connection():
    return oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}",
        protocol="tcps",
    )


    
