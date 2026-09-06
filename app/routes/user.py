from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.models.user import User
from app.utils.jwt import current_user_id

user_bp = Blueprint("user", __name__)


@user_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user = User.query.get(current_user_id())

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    ), 200
