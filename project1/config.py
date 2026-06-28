class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # IMPORTANT: JWT requires this exact key name
    JWT_SECRET_KEY = 'super-secret-key'
