from flask import Blueprint, render_template, redirect, url_for, session, make_response

public_bp = Blueprint("public_pages", __name__)


@public_bp.route("/")
def home():
    return render_template("home.html")


@public_bp.route("/login")
def login():
    if "user" in session:
        return redirect(url_for("web.private_pages.dashboard"))
    else:
        return render_template("login.html")


@public_bp.route("/signup")
def signup():
    if "user" in session:
        return redirect(url_for("web.private_pages.dashboard"))
    else:
        return render_template("signup.html")


@public_bp.route("/reset-password")
def reset_password():
    if "user" in session:
        return redirect(url_for("web.private_pages.dashboard"))
    else:
        return render_template("forgot_password.html")


@public_bp.route("/terms")
def terms():
    return render_template("terms.html")


@public_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")


@public_bp.route("/logout")
def logout():
    session.pop("user", None)  # Remove the user from session
    response = make_response(redirect(url_for("web.public_pages.login")))
    response.set_cookie("session", "", expires=0)  # Optionally clear the session cookie
    return response
