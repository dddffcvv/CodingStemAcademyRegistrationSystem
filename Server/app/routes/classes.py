from db_connection import get_db_connection
from flask import Blueprint, request, jsonify

classes_bp = Blueprint('classes', __name__)

# GET functions
@classes_bp.route('/classes', methods=['GET'])
def get_classes():
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM classes")
        res = cursor.fetchall()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({'message': 'All classes retrieved', 'classes': res})

@classes_bp.route('/all-classes-by-student', methods=['GET'])
def get_all_classes_by_student():
    user_id = request.args.get('student_id')
    db = get_db_connection()
    try:
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
    finally:
        db.close()
        cursor.close()
    return jsonify({'message': 'Classes retrieved', 'classes': classes})

@classes_bp.route('/all-classes-by-teacher', methods=['GET'])
def get_classes_by_teacher():
    id = request.args.get('teacher_id')
    db = get_db_connection()
    try:
        cursor = db.cursor(dictionary=True)
        sql = "SELECT * FROM classes WHERE teacher_id = %s"
        val = (id, )
        cursor.execute(sql, val)
        res = cursor.fetchall()
    finally:
        db.close()
        cursor.close()
    return jsonify({'message': 'Classes retrieved', 'classes': res})


@classes_bp.route('/class/<int:id>', methods=['GET'])
def get_class(id):
    db = get_db_connection()
    try:
        cursor = db.cursor(dictionary=True)
        sql = "SELECT * FROM classes WHERE id = %s"
        val = (id, )
        cursor.execute(sql, val)
        res = cursor.fetchone()
    finally:
        db.close()
        cursor.close()
    return jsonify({'message': 'Class retrieved', 'class': res})


# POST functions


@classes_bp.route('/add_class', methods=['POST'])
def add_class():
    data = request.get_json()
    teacher_id = data.get('teacher_id')
    class_name = data.get('class_name')
    subject = data.get('subject')
    semester_id = data.get('semester_id')

    my_db = get_db_connection()
    cursor = my_db.cursor()
    sql = "INSERT INTO classes (teacher_id, class_name, subject, semester_id) VALUES(%s, %s, %s, %s)"
    vals = (teacher_id, class_name, subject, semester_id)
    cursor.execute(sql, vals)
    my_db.commit()
    return jsonify({'message': 'Class has been added successfully'})


# PUT functions
@classes_bp.route('/update_class/<int:id>', methods=['PUT'])
def update_class(id):
    data = request.get_json()
    teacher_id = data.get('teacher_id')
    class_name = data.get('class_name')
    subject = data.get('subject')
    semester_id = data.get('semester_id')
    my_db = get_db_connection()
    try:
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
    finally:
        cursor.close()
        my_db.close()
    return jsonify({'message': 'Class was changed'})

# DELETE functions
@classes_bp.route('/delete_class/<int:id>', methods=['DELETE'])
def delete_class(id):
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor()
        sql = "DELETE FROM classes WHERE id = %s"
        val = (id, )
        cursor.execute(sql, val)
        my_db.commit()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({'message': 'Class has been deleted'})
