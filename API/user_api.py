from flask import Blueprint, request, jsonify, session, abort
from COMMON.config import logger, DB
from COMMON.error_handler import register_error_handlers_api
from COMMON.decorators import auth_required
from COMMON.common import create_user_document

user_api = Blueprint("user_api", __name__)
register_error_handlers_api(user_api)


def register_user_in_db(uid: str, email: str, display_name: str = None):
    """
    Create or update user document in Firestore
    Returns tuple of (success, message, status_code)
    """
    try:
        # Check if user exists in Firestore
        user_doc = DB.collection("users").document(uid).get()
        if user_doc.exists:
            return False, "User already exists in database", 409

        # Create user document in Firestore
        user_data = create_user_document(
            uid=uid, email=email, display_name=display_name
        )
        DB.collection("users").document(uid).set(user_data)
        logger.info(f"Created Firestore document for user {uid}")
        return True, "User document created successfully", 201
    except Exception as e:
        logger.error(f"Error creating user document: {str(e)}")
        return False, f"Database error: {str(e)}", 500


@user_api.route("/profile/", methods=["GET"])
@auth_required
def get_user():
    """Get the current user's information from database."""
    try:
        uid = session.get("user")["uid"]
        user = DB.collection("users").document(uid).get().to_dict()
        if not user:
            return jsonify({"error": "User not found in database"}), 404
        return jsonify(user), 200
    except Exception as e:
        logger.error(f"Error fetching user profile: {str(e)}")
        abort(500, str(e))


@user_api.route("/update/", methods=["PUT"])
@auth_required
def update_user():
    """Update the current user's information in database."""
    try:
        uid = session.get("user")["uid"]
        user = DB.collection("users").document(uid).get().to_dict()
        if not user:
            return jsonify({"error": "User not found in database"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Update user in Firestore
        DB.collection("users").document(uid).update(data)
        logger.info(f"Updated user {uid} in database")
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        abort(500, str(e))
