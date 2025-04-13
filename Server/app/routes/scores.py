from db_connection import get_db_connection
from flask import Blueprint, request, jsonify

scores_bp = Blueprint('scores', __name__)

# GET functions
@scores_bp.route('/scores', methods=['GET'])
def get_scores():
    connection = get_db_connection()
    try: 
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM scores")
        scores = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    return jsonify({'message': 'Scores retrieved successfully', 'scores': scores}), 200


@scores_bp.route('/scores/<int:assignment_id>/student/<int:student_id>', methods=['GET'])
def get_scores_by_student(assignment_id, student_id):
    connection = get_db_connection()
    try: 
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM scores WHERE student_id = %s AND assignment_id = %s", (student_id, assignment_id))
        scores = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    return jsonify({'message': 'Scores retrieved successfully', 'scores': scores}), 200
    

@scores_bp.route('/score', methods=['GET'])
def get_score():
    score_id = request.args.get('id')
    connection = get_db_connection()
    try: 
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM scores WHERE id = %s", (score_id,))
        score = cursor.fetchone()
    finally:
        cursor.close()
        connection.close()
    if score:
        return jsonify({'message': 'Score retrieved successfully', 'score': score}), 200
    else:
        return jsonify({'message': 'Score not found'}), 404
    
@scores_bp.route('/scores/assignment', methods=['GET'])
def get_scores_by_assignment():
    assignment_id = request.args.get('assignment_id')
    connection = get_db_connection()
    try: 
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM scores WHERE assignment_id = %s", (assignment_id,))
        scores = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    if scores:
        return jsonify({'message': 'Scores retrieved successfully', 'scores': scores}), 200
    else:
        return jsonify({'message': 'No scores found for this assignment'}), 404
