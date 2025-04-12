from db_connection import get_db_connection
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import request, jsonify, Blueprint
import bcrypt

users_bp = Blueprint('users', __name__)


# GET functions
@users_bp.route('/users', methods=['GET'])
def get_users():
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        res = cursor.fetchall()
    finally:
        my_db.close()
        cursor.close()
    return jsonify({"message": "Retrieved All Users", "users": res})

@users_bp.route('/users/by-name', methods=['GET'])
def get_user_by_name():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    db = get_db_connection()
    try:
        cursor = my_db.cursor(dictionary=True)
        sql = "SELECT * FROM users WHERE first_name = %s AND last_name = %s"
        val = (first_name, last_name)
        cursor.execute(sql, val)
        users = cursor.fetchall()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({"message": "Retrieved All Users by name", "users": users})

@users_bp.route('/user', methods=['GET'])
def get_user_by_id():
    id = request.args.get('id')
    db = get_db_connection()
    try:
        cursor = db.cursor(dictionary=True)
        sql = "SELECT * FROM users WHERE id = %s"
        val = (id, )
        cursor.execute(sql, val)
        user = cursor.fetchone()
    finally:
        db.close()
        cursor.close()
    return jsonify({"message": "User retrieved", "user": user})

@users_bp.route('/get-teacher-by-class', methods=['GET'])
def get_teacher_by_class():
    id = request.args.get('class_id')
    db = get_db_connection()
    try:
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
    finally:
        db.close()
        cursor.close()
    if teacher is None:
        return jsonify({"message": "Teacher not found"})
    return jsonify({"message": "Teacher retrieved", "teacher": teacher})

# POST functions
def add_auth(user_id, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    my_db = get_db_connection()
    cursor = my_db.cursor()
    sql = "INSERT INTO auths (user_id, password) VALUES (%s, %s)"
    vals = (user_id, hashed_password)
    cursor.execute(sql, vals)
    my_db.commit()
    return jsonify({"message": "Auth added"})


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    my_db = get_db_connection()
    try:
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
    finally:
        cursor.close()
        my_db.close()
    return jsonify({"message": "Login successful", "access_token": access_token})

@users_bp.route('/register', methods=['POST'])
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

    my_db = get_db_connection()
    cursor = my_db.cursor()
    sql = "INSERT INTO users " \
    "(first_name, last_name, birth_date, gender, email, phone, address, guardian, guardian_phone, health_ins, " \
    "health_ins_num, role, grade_level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    vals = (first_name, last_name, birth_date, gender, email, phone, address, guardian, guardian_phone,
             health_ins, health_ins_num, role, grade_level)
    cursor.execute(sql, vals)
    my_db.commit()
    user_id = cursor.lastrowid
    add_auth(user_id, data.get('password'))
    cursor.close()

    user_info = {
        "id": user_id,
        'email': email,
        'role': role,
        'first_name': first_name,
        'last_name': last_name,
    }

    access_token = create_access_token(identity=user_info)
    return jsonify({"message": "Login successful", "access_token": access_token})

def add_auth(user_id, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor = my_db.cursor()
    sql = "INSERT INTO auths (user_id, password) VALUES (%s, %s)"
    vals = (user_id, hashed_password)
    cursor.execute(sql, vals)
    my_db.commit()
    return jsonify({"message": "Auth added"})

# POST functions
@users_bp.route('/users/update', methods=['PUT'])
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

    my_db = get_db_connection()
    try:
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
    finally:
        cursor.close()
        my_db.close()
    return jsonify({"message": "User updated"})

# DELETE functions
@users_bp.route('/users', methods=['DELETE'])
def delete_user():
    id = request.args.get('id')
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor()
        sql = "DELETE FROM users WHERE id = %s"
        val = (id, )
        cursor.execute(sql, val)
        my_db.commit()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({"message": "User deleted"})
