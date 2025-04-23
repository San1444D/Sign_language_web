from flask import Blueprint, request, jsonify, session, abort
from firebase_admin import auth, firestore
from config import logger, reCAPTCHA_SECRET
from error_handler import register_error_handlers_api
import requests

auth_bp = Blueprint("auth", __name__)


register_error_handlers_api(auth_bp)


@auth_bp.route("/auth_login", methods=["POST"])
def authorize():
    token = request.headers.get("Authorization")
    reCapToken = request.headers.get("reCAPTCHA")
    if not token or not token.startswith("Bearer "):
        raise Exception("Authorization token is required with Bearer prefix")

    token = token[7:]  # Strip off 'Bearer ' to get the actual token

    try:
        if not reCapToken:
            raise Exception("reCAPTCHA token is required")
        reCapResponse = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": reCAPTCHA_SECRET["SECRET_KEY"], "response": reCapToken},
        )

        if reCapResponse.status_code != 200 or not reCapResponse.json().get("success"):
            raise Exception("reCAPTCHA verification failed")

        decoded_token = auth.verify_id_token(
            token, check_revoked=True
        )  # Validate token here

        session["user"] = decoded_token  # Add user to session
        session.permanent = True  # Make the session permanent
        return jsonify({"message": "Authorized Success"}), 200
    except Exception as e:
        logger.error(f"Authorization error: {e}")
        abort(401, e)
        return jsonify({"error": f"Unauthorized: {str(e)}"}), 401
