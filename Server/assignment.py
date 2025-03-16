import mysql.connector
from flask import Flask, request, jsonify

my_db = mysql.connector.connect(
    host="192.168.50.210",
    user="class_user",
    password="password",
    database="Registration"
)


def add_assignment(id, class_id, description, due_date):
    cursor = my_db.cursor()
    sql = "INSERT INTO assignments " \
    "(id, class_id, description, due_date, " \
    "VALUES (%s, %s, %s, %s)"
    vals = (id, class_id, description, due_date)
    cursor.execute(sql, vals)
    my_db.commit()



def get_assignment():
    cursor = my_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM assignments")
    return cursor.fetchall()


def get_assignment_by_id(id):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM assignments WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    return cursor.fetchone()


def update_assignment(id, class_id, description, due_date):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM assignments WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    assignment = cursor.fetchone()
    if assignment is None:
        return None
    sql = "UPDATE assignments SET class_id = %s, description" \
    " = %s, due_date = %s, WHERE id = %s"
    vals = (class_id if class_id else assignment["class_id"], description if description else assignment["description"], 
            due_date if due_date else assignment["due_date"], id)
    cursor.execute(sql, vals)
    my_db.commit()
    return cursor.fetchone()

def delete_assignment(id):
    cursor = my_db.cursor()
    sql = "DELETE FROM assignments WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    my_db.commit()


if __name__ == '__main__':
    if my_db.is_connected():
        print("Connected to MySQL Database")
    else:
        print("Failed to connect to MySQL Database")
