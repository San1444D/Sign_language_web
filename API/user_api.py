from flask import Blueprint, request, jsonify, session, redirect, url_for, abort
from firebase_admin import auth
from config import logger, DB
from error_handler import register_error_handlers_api
from decorators import auth_required

user_api = Blueprint("user_api", __name__)
register_error_handlers_api(user_api)


user_api.route("/register/", methods=["POST"])
@auth_required
def register_user():
    """
    Register a new user.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        # Create user in Firebase Auth
        user = auth.create_user(
            email=data["email"],
            password=data["password"],
            display_name=data.get("display_name"),
            disabled=False,
        )
        logger.info(f"User {user.uid} created successfully.")

        # Store user information in Firestore
        DB.collection("users").document(user.uid).set({
            "email": data["email"],
            "display_name": data.get("display_name"),
            "uid": user.uid,
        })
        return jsonify({"message": "User registered successfully"}), 200
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        abort(500)

@user_api.route("/profile/", methods=["GET"])
@auth_required
def get_user():
    """
    Get the current user's information.
    """
    try:
        uid = session.get("user")['uid']
        user = DB.collection("users").document(uid).get().to_dict()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # raise Exception("User Test")

        return jsonify(user), 200
    except Exception as e:
        logger.error(f"Error fetching user profile: {str(e)}")
        abort(401, e)

@user_api.route("/update/", methods=["PUT"])
@auth_required
def update_user():
    """
    Update the current user's information.
    """
    uid = session.get("user")['uid']
    user = DB.collection("users").document(uid).get().to_dict()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Update user information in Firebase Auth
    try:
        with DB.batch() as batch:
            # Update user in Firestore
            user_ref = DB.collection("users").document(uid)
            batch.update(user_ref, data)

            # Update user in Firebase Auth if email is provided
            if "email" in data:
                auth.update_user(uid, email=data["email"])
                logger.info(f"User {uid} email updated to {data['email']}")
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        abort(500)  # Internal Server Error

