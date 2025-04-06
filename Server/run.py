import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt

my_db = mysql.connector.connect(
    host="127.0.0.1",  # use at home
#     host="192.168.50.210", # use at school
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
    return jsonify({"message": "Retrieved All Users", "users": cursor.fetchall()})

def get_class_students():
    cursor = my_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM class_students")
    return cursor.fetchall()

@app.route('/classes', methods=['GET'])
def get_classes():
    cursor = my_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM classes")
    return jsonify({'message': 'All classes retrieved', 'classes': cursor.fetchall()})

@app.route('/classes/<int:id>', methods=['GET'])
def get_class(id):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM classes WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    return jsonify({'message': 'Class retrieved', 'classes': cursor.fetch()})

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

@app.route('/all-classes-by-student', methods=['GET'])
def get_all_classes_by_student():
    user_id = request.args.get('student_id')
    cursor = my_db.cursor(dictionary=True)
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
    return jsonify({'message': 'Classes retrieved', 'classes': classes})

@app.route('/classes/teachers/<int:id>', methods=['GET'])
def get_classes_by_teacher(id):
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM classes WHERE teacher_id = %s"
    val = (id, )
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
    return jsonify({"message": "Retrieved All Users by name", "users": cursor.fetchall()})

@app.route('/users', methods=['GET'])
def get_user_by_id():
    id = request.args.get('id')
    cursor = my_db.cursor(dictionary=True)
    sql = "SELECT * FROM users WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    return jsonify({"message": "User retrieved", "user": cursor.fetchone()})


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
    
#DELETE classes
@app.route('/delete_class/<int:id>', methods=['DELETE'])
def delete_class(id):
    cursor = my_db.cursor()
    sql = "DELEzTE FROM classes WHERE id = %s"
    val = (id, )
    cursor.execute(sql, val)
    my_db.commit()
    return jsonify({'message': 'Class has been deleted'})

if __name__ == '__main__':
    if my_db.is_connected():
        print("Connected to MySQL Database")
        app.run(debug=True)
    else:
        print("Failed to connect to MySQL Database")
