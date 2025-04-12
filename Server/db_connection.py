import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",  # use at home
        # host="192.168.50.210", # use at school
        user="class_user",
        password="password",
        database="Registration",
        connection_timeout=1000
    )
