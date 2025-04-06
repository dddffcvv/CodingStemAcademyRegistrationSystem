import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import logging
import bcrypt

from app import create_app

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
    return jsonify({"message": "Retrieved All Users", "users": cursor.fetchall()})

def get_class_students():
    cursor = my_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM class_students")
    return cursor.fetchall()


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



# Set up logging
logging.basicConfig(level=logging.DEBUG)

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

if __name__ == '__main__':
    port = 5000
    print(f"App is running on port {port}")
    app.run(debug=True, port=port)
