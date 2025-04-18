from flask import Blueprint, request, jsonify, session, redirect, url_for, abort
from firebase_admin import auth
from config import logger
from error_handler import register_error_handlers_api
from decorators import auth_required

user_api = Blueprint("user_api", __name__)
register_error_handlers_api(user_api)

@user_api.route("/profile", methods=["GET"])
@auth_required
def get_user():
    """
    Get the current user's information.
    """
    user = session.get("user")
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200

@user_api.route("/update", methods=["PUT"])
@auth_required
def update_user():
    """
    Update the current user's information.
    """
    user = session.get("user")
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Update user information in Firebase Auth
    try:
        auth.update_user(user["uid"], **data)
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        abort(500)  # Internal Server Error

