from flask import Blueprint, request, jsonify

from app.services.auth_service import register_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    result, status = register_user(
        username,
        email,
        password
    )

    return jsonify(result), status