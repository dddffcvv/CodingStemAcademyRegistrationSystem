from db_connection import get_db_connection
from flask import Blueprint, request, jsonify
from datetime import timedelta, time

classes_bp = Blueprint('classes', __name__)

def format_time(time_obj):
    if isinstance(time_obj, timedelta):
        # Convert timedelta to seconds and then to a time object
        total_seconds = time_obj.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        time_obj = time(hours, minutes)
    return time_obj.strftime("%I:%M %p")

# GET functions
@classes_bp.route('/classes', methods=['GET'])
def get_classes():
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM classes")
        res = cursor.fetchall()
        for classData in res:
            if 'start_time' in classData and isinstance(classData['start_time'], timedelta):
                classData['start_time'] = format_time(classData['start_time'])
            if 'end_time' in classData and isinstance(classData['end_time'], timedelta):
                classData['end_time'] = format_time(classData['end_time'])
    finally:
        cursor.close()
        my_db.close()
    return jsonify({'message': 'All classes retrieved', 'classes': res})

@classes_bp.route('/all-classes-by-student', methods=['GET'])
def get_all_classes_by_student():
    db = get_db_connection()
    try:
        user_id = request.args.get('student_id')
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
                class_info['student_id'] = user_id
                
                # Convert timedelta fields (if any) to strings
                if 'start_time' in class_info and isinstance(class_info['start_time'], timedelta):
                    class_info['start_time'] = format_time(class_info['start_time'])
                if 'end_time' in class_info and isinstance(class_info['end_time'], timedelta):
                    class_info['end_time'] = format_time(class_info['end_time'])

                
                if class_info:
                    classes.append(class_info)
    finally:
        db.close()
        cursor.close()
    if not classes:
        return jsonify({'message': 'No classes found for this student', 'classes': []})
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
        for classData in res:
            print(classData)
            if 'start_time' in classData and isinstance(classData['start_time'], timedelta):
                classData['start_time'] = format_time(classData['start_time'])
            if 'end_time' in classData and isinstance(classData['end_time'], timedelta):
                classData['end_time'] = format_time(classData['end_time'])
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
        if res is None:
            return jsonify({'message': 'Class not found'}), 404
        if 'start_time' in res and isinstance(res['start_time'], timedelta):
            res['start_time'] = format_time(res['start_time'])
        if 'end_time' in res and isinstance(res['end_time'], timedelta):
            res['end_time'] = format_time(res['end_time'])
    finally:
        db.close()
        cursor.close()
    return jsonify({'message': 'Class retrieved', 'class': res})


# POST functions


@classes_bp.route('/add-class', methods=['POST'])
def add_class():
    my_db = get_db_connection()
    data = request.get_json()
    try: 
        teacher_id = data.get('teacher_id')
        class_name = data.get('class_name')
        subject = data.get('subject')
        semester_id = data.get('semester_id')
        day = data.get('day')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        cursor = my_db.cursor()
        sql = "INSERT INTO classes (teacher_id, class_name, subject, semester_id, day, start_time, end_time) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        vals = (teacher_id, class_name, subject, semester_id, day, start_time, end_time)
        cursor.execute(sql, vals)
        my_db.commit()
    
        return jsonify({'message': 'Class has been added successfully'})
    except Exception as e:
        my_db.rollback()
        return jsonify({'message': 'Error occurred while adding class', 'error': str(e)}), 500
    finally:
        cursor.close()
        my_db.close()


# PUT functions
@classes_bp.route('/update_class/<int:id>', methods=['PUT'])
def update_class(id):
    data = request.get_json()
    teacher_id = data.get('teacher_id')
    class_name = data.get('class_name')
    subject = data.get('subject')
    semester_id = data.get('semester_id')
    day = data.get('day')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor()
        sql = "SELECT * FROM classes WHERE id = %s"
        val = (id, )
        cursor.execute(sql, val)
        classes = cursor.fetchone()
        if classes is None:
            return None
        sql = "UPDATE classes SET teacher_id = %s, class_name = %s, subject = %s, semester_id = %s, day = %s, start_time = %s, end_time = %s WHERE id = %s"
        vals = (
            teacher_id if teacher_id else classes["teacher_id"], class_name if class_name else classes["class_name"], 
            subject if subject else classes["subject"], semester_id if semester_id else classes["semester_id"],
            day if day else classes["day"], start_time if start_time else classes["start_time"], end_time if end_time else classes["end_time"], id
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
