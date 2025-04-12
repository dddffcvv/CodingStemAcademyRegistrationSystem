import mysql.connector

my_db = mysql.connector.connect(
    host="localhost",
#     host="192.168.50.210",
    user="class_user",
    password="password",
    database="Registration"
)


# ------------ CLASS STUDENT -----------------
def add_class_students(user_id, class_id):
    cursor = my_db.cursor()
    sql = "INSERT INTO class_students " \
    "(user_id, class_id) VALUES (%s, %s)"
    vals = (user_id, class_id)
    cursor.execute(sql, vals)
    my_db.commit()
def get_users():
    cursor = my_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM class_students")
    return cursor.fetchall()
def get_user_by_id(user_id):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM class_students WHERE id = %s"
    val = (user_id, )
    cursor.execute(sql, val)
    return cursor.fetchone()
def get_class_by_id(class_id):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM class_students WHERE id = %s"
    val = (class_id, )
    cursor.execute(sql, val)
    return cursor.fetchone()
def update_class_students(class_id, user_id):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM class_students WHERE id = %s"
    val = (class_id, user_id)
    cursor.execute(sql, val)
    user = cursor.fetchone()
    if user is None:
        return None
    sql = "UPDATE users SET user_id = %s, student_id = %s"
    vals = (user_id if user_id else user["user_id"], class_id if class_id else user["class_id"])
    cursor.execute(sql, vals)
    my_db.commit()
    return cursor.fetchone()
def delete_user_id(user_id):
    cursor = my_db.cursor()
    sql = "DELETE FROM class_students WHERE id = %s"
    val = (user_id, )
    cursor.execute(sql, val)
    my_db.commit()
def delete_class_id(class_id):
    cursor = my_db.cursor()
    sql = "DELETE FROM class_students WHERE id = %s"
    val = (class_id, )
    cursor.execute(sql, val)
    my_db.commit()


#------------ CLASS ---------------------------

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

def get_classes_by_teacher_id(teacher_id):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM classes WHERE teacher_id = %s"
    val = (teacher_id, )
    cursor.execute(sql, val)
    return cursor.fetchall()

def get_class_by_id(id):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM class_students WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    return cursor.fetchone()

def get_classes_by_id(id):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM class_students WHERE user_id = %s"
    val = (id, )
    cursor.execute(sql, val)
    return cursor.fetchall()

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

#------------ ASSIGNMENTS

def add_assignment(class_id, description, due_date):
    cursor = my_db.cursor()
    sql = "INSERT INTO assignments " \
    "(class_id, description, due_date) " \
    "VALUES (%s, %s, %s)"
    vals = (class_id, description, due_date)
    cursor.execute(sql, vals)
    my_db.commit()



def get_assignment():
    cursor = my_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM assignments")
    return cursor.fetchall()

def get_assignments_by_class(class_id):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM assignments WHERE class_id = %s"
    val = (class_id, )
    cursor.execute(sql, val)
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

