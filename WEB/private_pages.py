from flask import Blueprint, render_template
from decorators import auth_required

private_bp = Blueprint("private_pages", __name__)


@private_bp.route("/dashboard")
@auth_required
def dashboard():
    return render_template("dashboard.html")
