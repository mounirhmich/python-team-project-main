from flask import jsonify


def error_response(message: str, status_code: int):
    return jsonify({"message": message}), status_code


def success_response(message: str, status_code: int = 200, **data):
    payload = {"message": message, **data}
    return jsonify(payload), status_code
