from flask import Flask, request, jsonify, redirect
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from config import Config
from models import db, User, URL
from utils import generate_short_code

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()


# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "URL Shortener API is running!"
    })


# -------------------------
# REGISTER
# -------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(
        username=data["username"],
        password=data["password"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201


# -------------------------
# LOGIN
# -------------------------
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    user = User.query.filter_by(username=data["username"]).first()

    if not user or user.password != data["password"]:
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({"token": token})


# -------------------------
# SHORTEN URL
# -------------------------
@app.route("/shorten", methods=["POST"])
@jwt_required()
def shorten_url():

    user_id = get_jwt_identity()

    data = request.get_json()

    long_url = data["long_url"]

    short_code = generate_short_code(long_url)

    if URL.query.filter_by(short_code=short_code).first():
        return jsonify({
            "short_url": request.host_url + short_code
        })

    url = URL(
        long_url=long_url,
        short_code=short_code,
        user_id=user_id,
    )

    db.session.add(url)
    db.session.commit()

    return jsonify({
        "short_url": request.host_url + short_code
    })


# -------------------------
# REDIRECT
# -------------------------
@app.route("/<short_code>")
def redirect_url(short_code):

    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({"error": "URL not found"}), 404

    url.clicks += 1
    db.session.commit()

    return redirect(url.long_url)


# -------------------------
# ANALYTICS
# -------------------------
@app.route("/stats/<short_code>")
@jwt_required()
def stats(short_code):

    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "long_url": url.long_url,
        "short_code": url.short_code,
        "clicks": url.clicks
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
