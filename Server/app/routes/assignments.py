from db_connection import get_db_connection
from flask import Flask, jsonify, request, Blueprint

assignments_bp = Blueprint('assignments', __name__)

# GET functions
@assignments_bp.route('/assignments', methods=['GET'])
def get_assignments_by_class_route():
    class_id = request.args.get('class_id', type=int)
    assignments = get_assignments_by_class(class_id)
    if assignments is None:
        return jsonify({"message": "No assignments found"})
    return jsonify({"message": "Assignment retrieved", "assignments": assignments})


def get_assignments_by_class(class_id):
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor(dictionary=True)
        sql = "SELECT * FROM assignments WHERE class_id = %s"
        val = (class_id, )
        cursor.execute(sql, val)
        res = cursor.fetchall()
    finally:
        cursor.close()
        my_db.close()
    return res

@assignments_bp.route('/assignment', methods=['GET'])
def get_assignment_by_id_route():
    id = request.args.get('id')
    assignment = get_assignment_by_id(id)
    if assignment is None:
        return jsonify({"message": "Assignment not found"})
    return jsonify({"message": "Assignment retrieved", "assignment": assignment})

def get_assignment_by_id(id):
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor(dictionary=True)
        sql = "SELECT * FROM assignments WHERE id = %s"
        val = (id, )
        cursor.execute(sql, val)
        res = cursor.fetchone()
    finally:
        cursor.close()
        my_db.close()
    return res

@assignments_bp.route('/classes-assignments', methods=['GET'])
def get_assignments_for_class(class_id):
    class_id = request.args.get('class_id', class_id)
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM assignments WHERE class_id = %s", (class_id,))
        assignments = cursor.fetchall()
    finally:
        cursor.close()
        my_db.close()
    return jsonify({"message": "Retrieved All Assignments", "assignments": assignments})

# POST functions
@assignments_bp.route('/assignments', methods=['POST'])
def add_assignment_route():
    data = request.get_json()
    class_id = data.get('class_id')
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')

    add_assignment(class_id, description, due_date)
    return jsonify({"message": "Assignment added"})

def add_assignment(class_id, description, due_date):
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor()
        sql = "INSERT INTO assignments " \
        "(class_id, description, due_date) " \
        "VALUES (%s, %s, %s)"
        vals = (class_id, description, due_date)
        cursor.execute(sql, vals)
        my_db.commit()
    finally:
        cursor.close()
        my_db.close()


@assignments_bp.route('/update-assignment', methods=['PUT'])
def update_assignment_route():
    data = request.get_json()
    id = data.get('id')
    class_id = data.get('class_id')
    description = data.get('description')
    due_date = data.get('due_date')

    assignment = update_assignment(id, class_id, description, due_date)
    if assignment is None:
        return jsonify({"message": "Assignment not found"})
    return jsonify({"message": "Assignment updated", "assignment": assignment})


def update_assignment(id, class_id, description, due_date):
    my_db = get_db_connection()
    try:
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
        res = cursor.fetchone()
    finally:
        cursor.close()
        my_db.close()
    return res

# DELETE functions
@assignments_bp.route('/assignment', methods=['DELETE'])
def delete_assignment_route():
    id = request.args.get('id')
    if not delete_assignment(id):
        return jsonify({"message": "Assignment not found"})
    return jsonify({"message": "Assignment deleted", "assignment": assignment})

def delete_assignment(id):
    my_db = get_db_connection()
    try:
        cursor = my_db.cursor()
        sql = "DELETE FROM assignments WHERE id = %s"
        val = (id, )
        cursor.execute(sql, val)
        my_db.commit()
    except:
        return False
    finally:
        cursor.close()
        my_db.close()
    return True

