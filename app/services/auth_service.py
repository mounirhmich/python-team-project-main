from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash

def register_user(username, email, password):

    existing = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing:
        return {"message": "User already exists"}, 400

    hashed = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        password=hashed
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "User created successfully"}, 201