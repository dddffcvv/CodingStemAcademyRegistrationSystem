import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt

my_db = mysql.connector.connect(
    host="localhost",
#     host="192.168.50.210",
    user="class_user",
    password="password",
    database="Registration"
)

app = Flask(__name__)
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
    return jsonify({"message": "User added"})



def add_class_students(class_id, user_id):
    cursor = my_db.cursor()
    sql = "INSERT INTO class_students (class_id, user_id) VALUES (%s, %s)"
    vals = (class_id, user_id)
    cursor.execute(sql, vals)
    my_db.commit()

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


# PUT Data
@app.route('/users/update', methods=['PUT'])
def update_user():
    data = request.get_json()
    id = data.get('id')
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

    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM users WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    user = cursor.fetchone()
    if user is None:
        return jsonify({"message": "User not found"})
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
    return jsonify({"message": "User updated"})


# DELETE Data
@app.route('/users', methods=['DELETE'])
def delete_user():
    id = request.args.get('id')
    cursor = my_db.cursor()
    sql = "DELETE FROM users WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    my_db.commit()
    return jsonify({"message": "User deleted"})

def delete_student_class(student_id, class_id):
    cursor = my_db.cursor()
    sql = "DELETE FROM class_students WHERE student_id = %s AND class_id = %s"
    val = (student_id, class_id)
    cursor.execute(sql, val)
    my_db.commit()


def get_db_connection():
    global my_db
    if not my_db.is_connected():
        my_db.reconnect()
    return my_db


if __name__ == '__main__':
    if my_db.is_connected():
        print("Connected to MySQL Database")
    else:
        print("Failed to connect to MySQL Database")
    app.run(debug=True)
