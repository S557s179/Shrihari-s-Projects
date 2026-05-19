from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from models.models import db, Problem

problem_bp = Blueprint(
    'problems',
    __name__
)

@problem_bp.route('/problems', methods=['POST'])
@jwt_required()
def create_problem():

    user_id = get_jwt_identity()

    data = request.get_json()

    problem = Problem(
        title=data['title'],
        difficulty=data['difficulty'],
        topic=data['topic'],
        user_id=user_id
    )

    db.session.add(problem)
    db.session.commit()

    return jsonify({
        "message": "Problem created"
    })

@problem_bp.route('/problems', methods=['GET'])
@jwt_required()
def get_problems():

    user_id = get_jwt_identity()

    problems = Problem.query.filter_by(
        user_id=user_id
    ).all()

    result = []

    for p in problems:

        result.append({
            "id": p.id,
            "title": p.title,
            "difficulty": p.difficulty,
            "topic": p.topic,
            "completed": p.completed
        })

    return jsonify(result)

@problem_bp.route(
    '/problems/<int:id>',
    methods=['PUT']
)
@jwt_required()
def update_problem(id):

    data = request.get_json()

    problem = Problem.query.get(id)

    if not problem:
        return jsonify({
            "error": "Problem not found"
        }), 404

    problem.completed = data['completed']

    db.session.commit()

    return jsonify({
        "message": "Problem updated"
    })

@problem_bp.route(
    '/problems/<int:id>',
    methods=['DELETE']
)
@jwt_required()
def delete_problem(id):

    problem = Problem.query.get(id)

    if not problem:
        return jsonify({
            "error": "Problem not found"
        }), 404

    db.session.delete(problem)
    db.session.commit()

    return jsonify({
        "message": "Problem deleted"
    })