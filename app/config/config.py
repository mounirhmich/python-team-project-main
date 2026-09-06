import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "python-team-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)

    SQLALCHEMY_DATABASE_URI = "sqlite:///team.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
