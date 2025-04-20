from db_connection import get_db_connection
from flask import jsonify, request, Blueprint

class_students_bp = Blueprint('class_students', __name__)

# GET functions
@class_students_bp.route('/class_students', methods=['GET'])
def get_class_students():
    my_db = get_db_connection()
    cursor = my_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM class_students")
    res = cursor.fetchall()
    cursor.close()
    return jsonify({'message': 'Class students retrieved', 'class_students': res})


@class_students_bp.route('/classes/students/<int:id>', methods=['GET'])
def get_students_by_class(id):
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor(dictionary=True)
        sql = "SELECT * FROM class_students WHERE class_id = %s"
        val = (id, )
        cursor.execute(sql, val)
        res = cursor.fetchall()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({'message': 'Students retrieved', 'students': res})

@class_students_bp.route('/student-classes', methods=['GET'])
def get_student_classes():
    my_db = get_db_connection()
    try:
        user_id = request.args.get('user_id')
        cursor = my_db.cursor(dictionary=True)
        sql = "SELECT * FROM class_students WHERE user_id = %s"
        val = (user_id, )
        cursor.execute(sql, val)
        res = cursor.fetchall()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({'message': 'Classes retrieved', 'classes': res})


 # POST functions
@class_students_bp.route('/add_student_to_class', methods=['POST'])
def add_class_students():
    try:
        data = request.get_json()
        class_id = data.get('class_id')
        user_id = data.get('user_id')

        if not class_id or not user_id:
            return jsonify({'message': 'class_id and user_id are required'}), 400

        my_db = get_db_connection()
        cursor = my_db.cursor()
        sql = "INSERT INTO class_students (class_id, user_id) VALUES (%s, %s)"
        vals = (class_id, user_id)
        cursor.execute(sql, vals)
        my_db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'message': 'An error occurred', 'error': str(err)}), 500
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500
    finally:
        cursor.close()
        my_db.close()
    return jsonify({'message': 'Student added to class successfully'}), 200


@class_students_bp.route('/add_multiple_classes_to_student', methods=['POST'])
def add_multiple_classes():
    data = request.get_json()
    classes = data.get('classes')
    user_id = data.get('user_id')
    if not classes:
        return jsonify({'message': 'No classes provided'}), 400
    try:
        my_db = get_db_connection()
        cursor = my_db.cursor()
        for class_id in classes:
            sql = "INSERT INTO class_students (class_id, user_id) VALUES (%s, %s)"
            vals = (class_id, user_id)
            cursor.execute(sql, vals)
            my_db.commit()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({'message': 'Students have been added to classes successfully'})

# DELETE functions
@class_students_bp.route('/delete_student_from_class', methods=['DELETE'])
def delete_student_class():
    student_id = request.args.get('student_id')
    class_id = request.args.get('class_id')
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor()
        sql = "DELETE FROM class_students WHERE student_id = %s AND class_id = %s"
        val = (student_id, class_id)
        cursor.execute(sql, val)
        my_db.commit()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({'message': 'Student deleted from class successfully'})
