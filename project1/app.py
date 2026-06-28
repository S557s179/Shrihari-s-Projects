from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config
from models.models import db

from routes.auth_routes import auth_bp
from routes.problem_routes import problem_bp

app = Flask(__name__)

# Load config
app.config.from_object(Config)

# Initialize DB
db.init_app(app)

# JWT setup
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(problem_bp)


@app.route('/')
def home():
    return {
        "message": "Interview Prep Tracker API"
    }
