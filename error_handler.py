from flask import render_template, request, abort
from config import logger
from common import get_user_ip


def register_error_handlers_web(app):
    """
    Register custom error handlers for the Flask WEB application.

    This function sets up custom error handlers for common HTTP errors
    (404 Not Found, 403 Forbidden, 500 Internal Server Error) and
    unhandled exceptions. Each handler logs the error details and
    attempts to render a corresponding custom error page.

    Args:
        app (Flask): The Flask application instance to which the error
        handlers will be registered.

    Handlers:
        - 404 Not Found: Logs the error and renders a custom 404 error page.
        - 403 Forbidden: Logs the error and renders a custom 403 error page.
        - 500 Internal Server Error: Logs the error details, including
          request information, and renders a custom 500 error page.
        - Exception: Catches all unhandled exceptions, logs the error
          details, and renders a custom 500 error page.
    """

    @app.errorhandler(404)
    def page_not_found(error):
        try:
            return render_template("errors/404.html"), 404
        except Exception as e:
            logger.error(f"Error rendering 404 page: {e}")
            abort(500)  # Internal Server Error

    @app.errorhandler(403)
    def forbidden(error):
        try:
            return render_template("errors/403.html"), 403
        except Exception as e:
            logger.error(f"Error rendering 403 page: {e}")
            abort(500)  # Internal Server Error

    @app.errorhandler(500)
    def internal_server_error(error):
        """
        Custom error handler for 500 Internal Server Error.
        Logs the error and returns a custom error page.
        """
        # Log the error details
        logger.error(
            f"{error} \n Request URL: {request.url} \n Request Method: {request.method} \n Request Headers: {str(request.headers).replace('\n', ' ')}"
        )
        return render_template("errors/500.html"), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        """
        Custom error handler for all unhandled exceptions.
        Logs the error and returns a custom error page.
        """
        # Log the error details
        logger.error(
            f"Unhandled Exception: {e} \n Request URL: {request.url} \n Request Method: {request.method} \n Request Headers: {str(request.headers).replace('\n', ' ')}"
        )
        return render_template("errors/500.html"), 500
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """
        Custom error handler for 500 Internal Server Error.
        Logs the error and returns a custom error page.
        """
        # Log the error details
        logger.error(
            f"{error} \n Request URL: {request.url} \n Request Method: {request.method} \n Request Headers: {str(request.headers).replace('\n', ' ')}"
        )
        return render_template("errors/500.html"), 500


def register_error_handlers_api(app):
    """
    Register custom error handlers for the Flask API application.

    This function sets up custom error handlers for common HTTP errors
    (404 Not Found, 403 Forbidden, 500 Internal Server Error) and
    unhandled exceptions. Each handler logs the error details and
    returns a JSON response with the error message.

    Args:
        app (Flask): The Flask application instance to which the error
        handlers will be registered.

    Handlers:
        - 404 Not Found: Logs the error and returns a JSON response with
          a 404 status code.
        - 403 Forbidden: Logs the error and returns a JSON response with
          a 403 status code.
        - 500 Internal Server Error: Logs the error details, including
          request information, and returns a JSON response with a 500 status code.
        - Exception: Catches all unhandled exceptions, logs the error
          details, and returns a JSON response with a 500 status code.
    """

    @app.errorhandler(401)
    def unauthorized(error):
        logger.error(f"UserIP:{get_user_ip()} ||| Unauthorized: {error}")
        return {"error": "Unauthorized", "details": str(error)}, 401

    @app.errorhandler(404)
    def page_not_found(error):
        logger.error(f"UserIP:{get_user_ip()} ||| Page not found: {error}")

        return {"error": "Page not found"}, 404

    @app.errorhandler(403)
    def forbidden(error):
        logger.error(f"UserIP:{get_user_ip()} ||| Forbidden: {str(error)}")
        return {"error": "Forbidden"}, 403

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(
            f"{error} \n Request URL: {request.url} \n Request Method: {request.method} \n Request Headers: {str(request.headers).replace('\n', ' ')}"
        )
        return {"error": "Internal server error"}, 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(
            f"Unhandled Exception: {error} \n Request URL: {request.url} \n Request Method: {request.method} \n Request Headers: {str(request.headers).replace('\n', ' ')}"
        )
        return {"error": "Internal server error"}, 500
