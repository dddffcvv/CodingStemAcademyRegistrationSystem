import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import logging
import bcrypt
from app import create_app

my_db = mysql.connector.connect(
    host="127.0.0.1",  # use at home
#     host="192.168.50.210", # use at school
    user="class_user",
    password="password",
    database="Registration"
)
# Set up logging
logging.basicConfig(level=logging.DEBUG)


app = create_app()
## TODO: CREATE REAL SECRET KEY
app.config["JWT_SECRET_KEY"] = "temporary secret key"
jwt = JWTManager(app)
CORS(app)

# POST Data
@app.route('/register', methods=['POST'])
def add_user():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    birth_date = data.get('birth_date')
    gender = data.get('gender')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    guardian = data.get('guardian')
    guardian_phone = data.get('guardian_phone')
    health_ins = data.get('health_ins')
    health_ins_num = data.get('health_ins_num')
    role = data.get('role')
    grade_level = data.get('grade_level', None)
    cursor = my_db.cursor()

    # TODO: Add validation for data

    sql = "INSERT INTO users " \
    "(first_name, last_name, birth_date, gender, email, phone, address, guardian, guardian_phone, health_ins, " \
    "health_ins_num, role, grade_level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    vals = (first_name, last_name, birth_date, gender, email, phone, address, guardian, guardian_phone,
             health_ins, health_ins_num, role, grade_level)
    cursor.execute(sql, vals)
    my_db.commit()
    user_id = cursor.lastrowid
    add_auth(user_id, data.get('password'))

    user_info = {
        "id": user_id,
        'email': email,
        'role': role,
        'first_name': first_name,
        'last_name': last_name,
    }

    access_token = create_access_token(identity=user_info)
    return jsonify({"message": "Login successful", "access_token": access_token})


def add_class_students(class_id, user_id):
    cursor = my_db.cursor()
    sql = "INSERT INTO class_students (class_id, user_id) VALUES (%s, %s)"
    vals = (class_id, user_id)
    cursor.execute(sql, vals)
    my_db.commit()


#POST Class
@app.route('/add_class', methods=['POST'])
def add_class():
    data = request.get_json()
    #teacher_id, class_name, subject, semester_id
    teacher_id = data.get('teacher_id')
    class_name = data.get('class_name')
    subject = data.get('subject')
    semester_id = data.get('semester_id')

    cursor = my_db.cursor()
    sql = "INSERT INTO classes (teacher_id, class_name, subject, semester_id) VALUES(%s, %s, %s, %s)"
    vals = (teacher_id, class_name, subject, semester_id)
    cursor.execute(sql, vals)
    my_db.commit()
    return jsonify({'message': 'Class has been added successfully'})

@app.route('/add_student_to_class', methods=['POST'])
def add_class_students():
    try:
        data = request.get_json()
        class_id = data.get('class_id')
        user_id = data.get('user_id')

        if not class_id or not user_id:
            return jsonify({'message': 'class_id and user_id are required'}), 400

        cursor = my_db.cursor()
        sql = "INSERT INTO class_students (class_id, user_id) VALUES (%s, %s)"
        vals = (class_id, user_id)
        cursor.execute(sql, vals)
        my_db.commit()
        return jsonify({'message': 'Student has been added to class successfully'})
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'message': 'An error occurred', 'error': str(err)}), 500
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500

@app.route('/add_multiple_classes_to_student', methods=['POST'])
def add_multiple_classes():
    data = request.get_json()
    classes = data.get('classes')
    user_id = data.get('user_id')
    if not classes:
        return jsonify({'message': 'No classes provided'}), 400
    cursor = my_db.cursor()
    for class_id in classes:
        sql = "INSERT INTO class_students (class_id, user_id) VALUES (%s, %s)"
        vals = (class_id, user_id)
        cursor.execute(sql, vals)
        my_db.commit()
    return jsonify({'message': 'Students have been added to classes successfully'})

###################### DO NOT TOUCH #######################################
def add_auth(user_id, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor = my_db.cursor()
    sql = "INSERT INTO auths (user_id, password) VALUES (%s, %s)"
    vals = (user_id, hashed_password)
    cursor.execute(sql, vals)
    my_db.commit()
    return jsonify({"message": "Auth added"})


# GET Data
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cursor = my_db.cursor(dictionary=True)
    # Check if user with email exists
    sql = "SELECT * FROM users WHERE email = %s"
    val = (email, )
    cursor.execute(sql, val)
    user = cursor.fetchone()
    if user is None:
        return jsonify({"message": "Invalid email or password"})
    # Check if password matches
    sql = "SELECT * FROM auths WHERE user_id = %s"
    val = (user['id'], )
    cursor.execute(sql, val)
    auth = cursor.fetchone()
    if auth is None or not bcrypt.checkpw(password.encode('utf-8'), auth['password'].encode('utf-8')):
        return jsonify({"message": "Invalid password"})

    user_info = {
        "id": user['id'],
        'email': user['email'],
        'role': user['role'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
    }

    access_token = create_access_token(identity=user_info)
    return jsonify({"message": "Login successful", "access_token": access_token})


@app.route('/users', methods=['GET'])
def get_users():
    cursor = my_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    res = cursor.fetchall()
    cursor.close()
    return jsonify({"message": "Retrieved All Users", "users": res})

def get_class_students():
    cursor = my_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM class_students")
    res = cursor.fetchall()
    cursor.close()
    return res

@app.route('/classes', methods=['GET'])
def get_classes():
    cursor = my_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM classes")
    return jsonify({'message': 'All classes retrieved', 'classes': cursor.fetchall()})


@app.route('/classes/students/<int:id>', methods=['GET'])
def get_students_by_class(id):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM class_students WHERE class_id = %s"
    val = (id, )
    cursor.execute(sql, val)
    return jsonify({'message': 'Students retrieved', 'students': cursor.fetchall()})

@app.route('/student-classes', methods=['GET'])
def get_student_classes():
    user_id = request.args.get('user_id')
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM class_students WHERE user_id = %s"
    val = (user_id, )
    cursor.execute(sql, val)
    return jsonify({'message': 'Classes retrieved', 'classes': cursor.fetchall()})

@app.route('/users/by-name', methods=['GET'])
def get_user_by_name():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM users WHERE first_name = %s AND last_name = %s"
    val = (first_name, last_name)
    cursor.execute(sql, val)
    users = cursor.fetchall()
    cursor.close()
    return jsonify({"message": "Retrieved All Users by name", "users": users})

@app.route('/user', methods=['GET'])
def get_user_by_id():
    id = request.args.get('id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    sql = "SELECT * FROM users WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    user = cursor.fetchone()
    cursor.close()
    return jsonify({"message": "User retrieved", "user": user})

@app.route('/classes', methods=['GET'])
def get_all_classes():
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM classes"
    cursor.execute(sql)
    classes = cursor.fetchall()
    cursor.close()
    return jsonify({"message": "Retrieved All Classes", "classes": classes})

@app.route('/get-teacher-by-class', methods=['GET'])
def get_teacher_by_class():
    id = request.args.get('class_id')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    sql = "SELECT * FROM classes WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    class_info = cursor.fetchone()
    if class_info is None:
        return jsonify({"message": "Class not found"})
    sql = "SELECT * FROM users WHERE id = %s"
    val = (class_info['teacher_id'], )
    cursor.execute(sql, val)
    teacher = cursor.fetchone()
    cursor.close()
    if teacher is None:
        return jsonify({"message": "Teacher not found"})
    return jsonify({"message": "Teacher retrieved", "teacher": teacher})


@app.route('/all-classes-by-student', methods=['GET'])
def get_all_classes_by_student():
    user_id = request.args.get('student_id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    sql = "SELECT * FROM class_students WHERE user_id = %s"
    vals = (user_id, )
    cursor.execute(sql, vals)
    student_classes = cursor.fetchall()
    classes = []
    for row in student_classes:
        if row['class_id'] not in classes:
            sql = "SELECT * FROM classes WHERE id = %s"
            val = (row['class_id'], )
            cursor.execute(sql, val)
            class_info = cursor.fetchone()
            if class_info:
                classes.append(class_info)
    cursor.close()
    return jsonify({'message': 'Classes retrieved', 'classes': classes})

@app.route('/all-classes-by-teacher', methods=['GET'])
def get_classes_by_teacher():
    id = request.args.get('teacher_id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    sql = "SELECT * FROM classes WHERE teacher_id = %s"
    val = (id, )
    cursor.execute(sql, val)
    res = cursor.fetchall()
    cursor.close()
    return jsonify({'message': 'Classes retrieved', 'classes': res})

@app.route('/class/<int:id>', methods=['GET'])
def get_class(id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    sql = "SELECT * FROM classes WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    res = cursor.fetchone()
    cursor.close()
    return jsonify({'message': 'Class retrieved', 'class': res})



#PUT Class
@app.route('/update_class/<int:id>', methods=['PUT'])
def update_class(id):
    data = request.get_json()
    teacher_id = data.get('teacher_id')
    class_name = data.get('class_name')
    subject = data.get('subject')
    semester_id = data.get('semester_id')


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
    return jsonify({'message': 'Class was changed', 'class': cursor.fetchone()})


@app.errorhandler(403)
def forbidden(e):
    logging.error(f"403 error: {e}")
    return jsonify({"message": "Forbidden: You don't have permission to access this resource"}), 403

def delete_student_class(student_id, class_id):
    cursor = my_db.cursor()
    sql = "DELETE FROM class_students WHERE student_id = %s AND class_id = %s"
    val = (student_id, class_id)
    cursor.execute(sql, val)
    my_db.commit()

#DELETE classes
@app.route('/delete_class/<int:id>', methods=['DELETE'])
def delete_class(id):
    cursor = my_db.cursor()
    sql = "DELEzTE FROM classes WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    my_db.commit()
    return jsonify({'message': 'Class has been deleted'})


def get_db_connection():
    global my_db
    if not my_db.is_connected():
        my_db.reconnect()
    return my_db


if __name__ == '__main__':
    port = 5000
    print(f"App is running on port {port}")
    app.run(debug=True, port=port)
