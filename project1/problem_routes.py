from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, Problem

problem_bp = Blueprint('problems', __name__)


@problem_bp.route('/problems', methods=['POST'])
@jwt_required()
def create_problem():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing data"}), 400

    user_id = get_jwt_identity()

    problem = Problem(
        title=data.get('title'),
        difficulty=data.get('difficulty'),
        topic=data.get('topic'),
        user_id=user_id
    )

    db.session.add(problem)
    db.session.commit()

    return jsonify({"message": "Problem created"})


@problem_bp.route('/problems', methods=['GET'])
@jwt_required()
def get_problems():
    user_id = get_jwt_identity()

    problems = Problem.query.filter_by(user_id=user_id).all()

    result = [{
        "id": p.id,
        "title": p.title,
        "difficulty": p.difficulty,
        "topic": p.topic,
        "completed": p.completed
    } for p in problems]

    return jsonify(result)


@problem_bp.route('/problems/<int:id>', methods=['PUT'])
@jwt_required()
def update_problem(id):
    data = request.get_json()

    problem = Problem.query.get(id)

    if not problem:
        return jsonify({"error": "Problem not found"}), 404

    if "completed" in data:
        problem.completed = data["completed"]

    db.session.commit()

    return jsonify({"message": "Problem updated"})


@problem_bp.route('/problems/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_problem(id):
    problem = Problem.query.get(id)

    if not problem:
        return jsonify({"error": "Problem not found"}), 404

    db.session.delete(problem)
    db.session.commit()

    return jsonify({"message": "Problem deleted"})
