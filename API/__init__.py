from flask import Blueprint
from flask import render_template, request, redirect, url_for, session
from error_handler import register_error_handlers_api

api = Blueprint(
    "api",
    __name__,
    static_folder="./../static",
    template_folder="./../templates",
)

register_error_handlers_api(api)

from .auth import auth_bp as auth_blueprint
from .model_api import model_bp as model_blueprint

api.register_blueprint(auth_blueprint, url_prefix="/auth")
api.register_blueprint(model_blueprint, url_prefix="/model")
