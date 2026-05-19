from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config
from models.models import db

from routes.auth_routes import auth_bp
from routes.problem_routes import problem_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

jwt = JWTManager(app)

# Register routes
app.register_blueprint(auth_bp)
app.register_blueprint(problem_bp)

@app.route('/')
def home():
    return {
        "message": "Interview Prep Tracker API"
    }

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)