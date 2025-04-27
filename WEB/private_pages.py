from flask import Blueprint, render_template
from COMMON.decorators import auth_required

private_bp = Blueprint("private_pages", __name__)


@private_bp.route("/dashboard")
@auth_required
def dashboard():
    return render_template("dashboard.html")

@private_bp.route("/to-gesture/")
@auth_required
def to_gesture():
    return render_template("to_gesture.html")

@private_bp.route("/to-text/")
@auth_required
def to_text():
    return render_template("to_text.html")