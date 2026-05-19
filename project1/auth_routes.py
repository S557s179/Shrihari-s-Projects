from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from models.models import db, User
from utils.auth_utils import (
    hash_password,
    check_password
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    existing_user = User.query.filter_by(
        username=data['username']
    ).first()

    if existing_user:
        return jsonify({
            "error": "Username already exists"
        }), 400

    user = User(
        username=data['username'],
        password=hash_password(data['password'])
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered"
    })

@auth_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    user = User.query.filter_by(
        username=data['username']
    ).first()

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    valid = check_password(
        data['password'],
        user.password
    )

    if not valid:
        return jsonify({
            "error": "Invalid password"
        }), 401

    token = create_access_token(
        identity=user.id
    )

    return jsonify({
        "token": token
    })