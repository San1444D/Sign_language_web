from flask import (
    Blueprint,
    render_template,
    stream_template,
    abort,
    session,
    redirect,
    url_for,
)
from COMMON.config import logger


web_routes = Blueprint(
    "web",
    __name__,
)


@web_routes.route("/", methods=["GET"])
def main_page():
    try:
        if session.get("logged_in"):
            return redirect(url_for("web.main.home_page"))
        return stream_template("main.html")
    except Exception as e:
        logger.error(f"Error rendering main page: {e}")
        abort(403)  # Internal Server Error


@web_routes.route("/login", methods=["GET"])
def login_page():
    try:
        return stream_template("login.html")
    except Exception as e:
        logger.error(f"Error rendering login page: {e}")
        abort(500)  # Internal Server Error
