from db_connection import get_db_connection
from flask import jsonify, request, Blueprint, json

submissions_bp = Blueprint('submissions', __name__)


# GET functions
@submissions_bp.route('/assignments-submissions', methods=['GET'])
def get_submissions_for_assignment():
    my_db = get_db_connection()
    try:
        assignment_id = request.args.get('assignment_id')
        cursor = my_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM submissions WHERE assignment_id = %s", (assignment_id,))
        submissions = cursor.fetchall()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({"message": "Retrieved All Submissions", "submissions": submissions})

def get_submissions_for_assignment(assignment_id):
    my_db = get_db_connection()
    try:
        assignment_id = request.args.get('assignment_id', assignment_id)
        cursor = my_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM submissions WHERE assignment_id = %s", (assignment_id,))
        submissions = cursor.fetchall()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({"message": "Retrieved All Submissions", "submissions": submissions})


@submissions_bp.route('/teacher-submissions', methods=['GET'])
def get_submissions_for_teacher():
    teacher_id = request.args.get('teacher_id')
    classes = json.loads(get_classes_for_teacher(teacher_id).data)['classes']
    assignments = []
    for class_dict in classes:
        res = json.loads(get_assignments_for_class(class_dict['id']).data)
        assignments.append(res['assignments'])
    submissions = []
    for assignment_list in assignments:
        for assignment in assignment_list:
            res = json.loads(get_submissions_for_assignment(assignment['id']).data)
            submissions.append(res['submissions'])
    return jsonify({
        "message": "Retrieved All Submissions",
        "submissions": submissions,
        "classes": classes,
        "assignments": assignments
    })

def get_classes_for_teacher(teacher_id):
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM classes WHERE teacher_id = %s", (teacher_id,))
        classes = cursor.fetchall()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({
        "message": "Retrieved Classes for Teacher",
        "classes": classes
    })

def get_assignments_for_class(class_id):
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM assignments WHERE class_id = %s", (class_id,))
        assignments = cursor.fetchall()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({
        "message": "Retrieved Assignments for Class",
        "assignments": assignments
    })

@submissions_bp.route('/student-submissions', methods=['GET'])
def get_submissions_for_student():
    student_id = request.args.get('student_id')

    # Get class IDs for the student
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM class_students WHERE user_id = %s", (student_id,))
        class_ids = [row['class_id'] for row in cursor.fetchall()]

        # Get class details
        classes = []
        if class_ids:
            cursor.execute("SELECT * FROM classes WHERE id IN (%s)" % ','.join(['%s'] * len(class_ids)), class_ids)
            classes = cursor.fetchall()

        # Get assignments for the classes
        assignments = []
        for class_dict in classes:
            res = json.loads(get_assignments_for_class(class_dict['id']).data)
            assignments.append(res['assignments'])
        submissions = []
        for assignment_list in assignments:
            for assignment in assignment_list:
                cursor.execute("SELECT * FROM submissions WHERE assignment_id = %s AND student_id = %s", (assignment['id'], student_id))
                res = cursor.fetchall()
                print(res)
                submissions.append(res)
    finally:
        my_db.close()
        cursor.close()

    return jsonify({
        "message": "Retrieved Submissions for Student",
        "classes": classes,
        "assignments": assignments,
        "submissions": submissions
    })

@submissions_bp.route('/submissions/student', methods=['GET'])
def get_submissions_by_class():
    assignment_id = request.args.get('assignment_id')
    student_id = request.args.get('student_id')
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM submissions WHERE assignment_id = %s AND student_id = %s", (assignment_id, student_id))
        submissions = cursor.fetchall()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({"message": "Retrieved All Submissions", "submissions": submissions})