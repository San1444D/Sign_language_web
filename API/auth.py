from flask import Blueprint, request, jsonify, session, abort
from firebase_admin import auth
from COMMON.config import logger, reCAPTCHA_SECRET
from COMMON.error_handler import register_error_handlers_api
from .user_api import register_user_in_db
import requests

auth_bp = Blueprint("auth", __name__)
register_error_handlers_api(auth_bp)


@auth_bp.route("/auth_login", methods=["POST"])
def authorize():
    """Handle user authentication and DB registration"""
    try:
        token = request.headers.get("Authorization")
        reCapToken = request.headers.get("reCAPTCHA")

        if not token or not token.startswith("Bearer "):
            abort(401, "Authorization token is required with Bearer prefix")
        if not reCapToken:
            abort(400, "reCAPTCHA token is required")

        token = token[7:]  # Strip off 'Bearer ' to get the actual token

        # Verify reCAPTCHA
        reCapResponse = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": reCAPTCHA_SECRET["SECRET_KEY"], "response": reCapToken},
        )

        if reCapResponse.status_code != 200 or not reCapResponse.json().get("success"):
            abort(401, "reCAPTCHA verification failed")

        # Verify Firebase token
        decoded_token = auth.verify_id_token(token, check_revoked=True)

        # Get user info from Firebase Auth
        firebase_user = auth.get_user(decoded_token["uid"])

        # Try to register user in database if they don't exist
        success, message, status_code = register_user_in_db(
            uid=firebase_user.uid,
            email=firebase_user.email,
            display_name=firebase_user.display_name,
        )

        if not success and status_code != 409:  # Ignore if user already exists
            logger.warning(f"Failed to create user document: {message}")

        session["user"] = decoded_token  # Add user to session
        session.permanent = True  # Make the session permanent
        return jsonify({"message": "Authorized Success"}), 200

    except auth.RevokedIdTokenError:
        abort(401, "Token has been revoked. Please re-authenticate")
    except auth.InvalidIdTokenError:
        abort(401, "Invalid token. Please re-authenticate")
    except auth.ExpiredIdTokenError:
        abort(401, "Token has expired. Please re-authenticate")
    except Exception as e:
        logger.error(f"Authorization error: {str(e)}")
        abort(401, str(e))
