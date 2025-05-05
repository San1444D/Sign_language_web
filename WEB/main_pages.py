from COMMON.config import logger
from flask import Blueprint, render_template, stream_template, abort
from flask import request, redirect, url_for, session
from COMMON.decorators import login_required


main_bp = Blueprint(
    "main",
    __name__,
)

@main_bp.route("/home", methods=["GET"])
def home_page():
    try:
        return stream_template("home.html")
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        abort(500)