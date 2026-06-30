import datetime

SECRET_KEY = "super-secret-key-change-this"
JWT_SECRET = "jwt-secret-change-this"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600

SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
