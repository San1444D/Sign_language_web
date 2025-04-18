from flask import Blueprint, request, redirect, url_for, session, abort
from firebase_admin import auth
from config import logger
from decorators import login_required
from error_handler import register_error_handlers_api

auth_bp = Blueprint("auth", __name__)


register_error_handlers_api(auth_bp)


@auth_bp.route("/auth_login", methods=["POST"])
def authorize():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return "Unauthorized", 401

    token = token[7:]  # Strip off 'Bearer ' to get the actual token

    try:
        decoded_token = auth.verify_id_token(
            token, check_revoked=True, clock_skew_seconds=60
        )  # Validate token here
        
        session["user"] = decoded_token  # Add user to session
        session.permanent = True  # Make the session permanent
        return redirect(
            url_for("web.private_pages.dashboard")
        )  # Redirect to dashboard after successful login

    except Exception as e:
        logger.error(f"Authorization error: {str(e)}")
        return f"Unauthorized: {str(e)}", 401
