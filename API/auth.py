from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from config import logger
from decorators import login_required
from error_handler import register_error_handlers_api

auth_bp = Blueprint(
    "auth",
    __name__,
    static_folder="./../static",
    template_folder="./../templates",
)


register_error_handlers_api(auth_bp)
