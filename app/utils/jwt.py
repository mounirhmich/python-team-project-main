from datetime import timedelta

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


def create_token(user_id: int) -> str:
    return create_access_token(identity=str(user_id), expires_delta=timedelta(hours=1))


def current_user_id() -> int:
    return int(get_jwt_identity())


__all__ = ["create_token", "current_user_id", "jwt_required"]
