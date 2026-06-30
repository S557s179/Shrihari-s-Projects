from flask import Blueprint, request, jsonify
import jwt
import bcrypt
import datetime
import config
from app import db
from models import User

auth_bp = Blueprint("auth", __name__)

def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=config.JWT_EXP_DELTA_SECONDS)
    }
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    hashed_pw = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())

    user = User(username=data["username"], password=hashed_pw.decode("utf-8"))
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return jsonify({"error": "Invalid user"}), 401

    if not bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
        return jsonify({"error": "Invalid password"}), 401

    token = create_token(user.id)

    return jsonify({"token": token})
