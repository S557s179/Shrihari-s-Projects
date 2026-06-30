from flask import Blueprint, request, jsonify
import jwt
import secrets
import hashlib
import datetime

import config
from app import db
from models import User, APIKey, UsageLog

api_bp = Blueprint("api", __name__)


# -------------------------
# AUTH HELPER
# -------------------------
def auth_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Missing token"}), 401

        try:
            decoded = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
            request.user_id = decoded["user_id"]
        except:
            return jsonify({"error": "Invalid token"}), 401

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


# -------------------------
# API KEY GENERATION
# -------------------------
@api_bp.route("/apikeys", methods=["POST"])
@auth_required
def create_key():
    raw_key = secrets.token_hex(16)
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

    api_key = APIKey(user_id=request.user_id, key_hash=key_hash)
    db.session.add(api_key)
    db.session.commit()

    return jsonify({"api_key": raw_key})


# -------------------------
# LIST KEYS
# -------------------------
@api_bp.route("/apikeys", methods=["GET"])
@auth_required
def get_keys():
    keys = APIKey.query.filter_by(user_id=request.user_id).all()

    return jsonify([
        {
            "id": k.id,
            "created_at": k.created_at,
            "revoked": k.revoked,
            "last_used": k.last_used
        }
        for k in keys
    ])


# -------------------------
# REVOKE KEY
# -------------------------
@api_bp.route("/apikeys/<int:key_id>", methods=["DELETE"])
@auth_required
def revoke_key(key_id):
    key = APIKey.query.get(key_id)

    if not key or key.user_id != request.user_id:
        return jsonify({"error": "Not found"}), 404

    key.revoked = True
    db.session.commit()

    return jsonify({"message": "Key revoked"})


# -------------------------
# VALIDATE API KEY (SIMULATES USAGE)
# -------------------------
@api_bp.route("/validate", methods=["POST"])
def validate_key():
    data = request.json
    raw_key = data.get("api_key")

    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

    key = APIKey.query.filter_by(key_hash=key_hash, revoked=False).first()

    if not key:
        return jsonify({"valid": False}), 401

    key.last_used = datetime.datetime.utcnow()

    log = UsageLog(key_id=key.id, endpoint="/validate")
    db.session.add(log)
    db.session.commit()

    return jsonify({"valid": True})
