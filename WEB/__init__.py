from flask import Blueprint


web = Blueprint(
    "web",
    __name__,
    static_folder="./../static",
    template_folder="./../templates",
)

from .web_routes import web_routes as web_routes_bp
from .main_pages import main_bp as main_pages_bp

web.register_blueprint(web_routes_bp)
web.register_blueprint(main_pages_bp)
