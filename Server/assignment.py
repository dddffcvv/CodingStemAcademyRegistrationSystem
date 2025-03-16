import mysql.connector
from flask import Flask, request, jsonify

my_db = mysql.connector.connect(
    host="192.168.50.210",
    user="class_user",
    password="password",
    database="Registration"
)

def classes(id, teacher_id, class_name, subject, semester_id):
    sql = "INSERT INTO classes " \
    "(id, teacher_id, class_name, subject, semester_id) VALUES (%s, %s, %s, %s, %s)"
    val = (id, teacher_id, class_name, subject, semester_id)
    cursor.execute(sql, vals)
    my_db.commit()

def get_class_by_name():
    cursor = my_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM class_name")
    return cursor.fetchall()

def get_class_by_id(id):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM class_name WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    return cursor.fetchone()

def update_class(id, teacher_id, class_name, subject, semester_id):
    cursor = my_db.cursor(dictionary=True)
    
    sql = "SELECT * FROM class_name WHERE id = %s"
    val = (id,)
    cursor.execute(sql, val)
    existing_class = cursor.fetchone()
    
    if existing_class is None:
        return None
    
    sql = """UPDATE class_name 
             SET teacher_id = %s, class_name = %s, subject = %s, semester_id = %s 
             WHERE id = %s"""
    vals = (teacher_id, class_name, subject, semester_id, id)
    cursor.execute(sql, vals)
    my_db.commit()
    
    return cursor.fetchone

def delete_class(id):
    cursor = my_db.cursor()
    sql = "DELETE FROM class_name WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    my_db.commit()


if __name__ == '__main__':
    if my_db.is_connected():
        print("Connected to MySQL Database")
    else:
        print("Failed to connect to MySQL Database")