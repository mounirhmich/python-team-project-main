from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from app.routes.auth import auth_bp

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config.from_object("app.config.config.Config")

    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    app.register_blueprint(auth_bp)

    return app
