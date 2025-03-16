import mysql.connector
from flask import Flask, request, jsonify

my_db = mysql.connector.connect(
    host="192.168.50.210",
    user="class_user",
    password="password",
    database="Registration"
)


# POST Data 
###################### DO NOT TOUCH #######################################
def add_user(first_name, last_name, birth_date, gender, 
             email, phone, address, guardian, guardian_phone, 
             health_ins, health_ins_num, role, grade_level = None):
    cursor = my_db.cursor()
    sql = "INSERT INTO users " \
    "(first_name, last_name, birth_date, gender, email, phone, address, guardian, guardian_phone, health_ins, " \
    "health_ins_num, role, grade_level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    vals = (first_name, last_name, birth_date, gender, email, phone, address, guardian, guardian_phone, 
             health_ins, health_ins_num, role, grade_level)
    cursor.execute(sql, vals)
    my_db.commit()

#POST Class
def add_class(teacher_id, class_name, subject, semester_id):
    cursor = my_db.cursor()
    sql = "INSERT INTO classes (teacher_id, class_name, subject, semester_id) VALUES(%s, %s, %s, %s)"
    vals = (teacher_id, class_name, subject, semester_id)
    cursor.execute(sql, vals)
    my_db.commit()

    





###################### DO NOT TOUCH #######################################
def add_auth(user_id, password):
    cursor = my_db.cursor()
    sql = "INSERT INTO auth (user_id, password) VALUES (%s, %s)"
    vals = (user_id, password)
    cursor.execute(sql, vals)
    my_db.commit()


# GET Data
###################### DO NOT TOUCH #######################################
def login(email, password):
    cursor = my_db.cursor(dictionary=True)
    # Check if user with email exists
    sql = "SELECT * FROM users WHERE email = %s"
    val = (email, )
    cursor.execute(sql, val)
    user = cursor.fetchone()
    if user is None:
        return None
    # Check if password matches
    sql = "SELECT * FROM auth WHERE user_id = %s AND password = %s"
    val = (user['id'], password)
    cursor.execute(sql, val)
    auth = cursor.fetchone()
    if auth is None:
        return None
    return user


###################### DO NOT TOUCH #######################################
def get_users():
    cursor = my_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


###################### DO NOT TOUCH #######################################
def get_user_by_name(first_name, last_name):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM users WHERE first_name = %s AND last_name = %s"
    val = (first_name, last_name)
    cursor.execute(sql, val)
    return cursor.fetchall()


###################### DO NOT TOUCH #######################################
def get_user_by_id(id):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM users WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    return cursor.fetchone()


# PUT Data 
###################### DO NOT TOUCH #######################################
def update_user(id, first_name, last_name, birth_date, gender, 
             email, phone, address, guardian, guardian_phone, 
             health_ins, health_ins_num, role, grade_level = None):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM users WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    user = cursor.fetchone()
    if user is None:
        return None
    sql = "UPDATE users SET first_name = %s, last_name = %s, birth_date" \
    " = %s, gender = %s, email = %s, phone = %s, address = %s, guardian = %s, guardian_phone = %s, health_ins = %s, " \
    "health_ins_num = %s, role = %s, grade_level = %s WHERE id = %s"
    vals = (first_name if first_name else user["first_name"], last_name if last_name else user["last_name"], 
            birth_date if birth_date else user["birth_date"], gender if gender else user["gender"], email if email else user["email"],
            phone if phone else user["phone"], address if address else user["address"], guardian if guardian else user["guardian"],
            guardian_phone if guardian_phone else user["guardian_phone"], health_ins if health_ins else user["health_ins"],
            health_ins_num if health_ins_num else user["health_ins_num"], role if role else user["role"],
            grade_level if grade_level else user["grade_level"], id)
    cursor.execute(sql, vals)
    my_db.commit()
    return cursor.fetchone()

#PUT Class
def update_class(id, teacher_id, class_name, subject, semester_id):
    cursor = my_db.cursor()
    sql = "SELECT * FROM classes WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    classes = cursor.fetchone()
    if classes is None:
        return None
    sql = "UPDATE classes SET teacher_id = %s, class_name = %s, subject = %s, semester_id = %s"
    vals = (
        teacher_id if teacher_id else classes["teacher_id"], class_name if class_name else classes["class_name"], subject if subject else classes["subject"], semester_id if semester_id else classes["semester_id"], id
    )
    cursor.execute(sql, vals)
    my_db.commit()
    return cursor.fetchone()





# DELETE Data
###################### DO NOT TOUCH #######################################
def delete_user(id):
    cursor = my_db.cursor()
    sql = "DELETE FROM users WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    my_db.commit()

#DELETE classes
def delete_class(id):
    cursor = my_db.cursor()
    sql = "DELETE FROM classes WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    my_db.commit()




if __name__ == '__main__':
    if my_db.is_connected():
        print("Connected to MySQL Database")
    else:
        print("Failed to connect to MySQL Database")

