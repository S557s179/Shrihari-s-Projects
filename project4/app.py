from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

# Import after db init to avoid circular imports
from auth import auth_bp
from routes import api_bp

app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)

with app.app_context():
    import models
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
