from flask import Blueprint
from flask import render_template, request, redirect, url_for, session
from COMMON.error_handler import register_error_handlers_api

api = Blueprint("api", __name__)

register_error_handlers_api(api)

from .auth import auth_bp as auth_blueprint
from .user_api import user_api as user_blueprint
from .model_api import model_bp as model_blueprint
from .get_api import get_api_bp as get_blueprint

api.register_blueprint(auth_blueprint, url_prefix="/auth")
api.register_blueprint(user_blueprint, url_prefix="/user")
api.register_blueprint(get_blueprint, url_prefix="/get")
api.register_blueprint(model_blueprint, url_prefix="/model")
