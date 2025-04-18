from flask import Blueprint
from error_handler import register_error_handlers_web


web = Blueprint(
    "web",
    __name__,
    static_folder="./../static",
    template_folder="./../templates",
)
register_error_handlers_web(web)

from .web_routes import web_routes as web_routes_bp
from .main_pages import main_bp as main_pages_bp

# web.register_blueprint(web_routes_bp)
# web.register_blueprint(main_pages_bp)


from .public_pages import public_bp as public_pages_bp
from .private_pages import private_bp as private_pages_bp

web.register_blueprint(public_pages_bp)
web.register_blueprint(private_pages_bp)