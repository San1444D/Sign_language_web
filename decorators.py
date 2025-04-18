from flask import session, redirect, url_for
from functools import wraps

"""
Custom decorators for the Flask application.
This module contains decorators for various purposes,
such as checking user authentication and authorization.
"""


def login_required(func):
    """
    Decorator to ensure the user is logged in before accessing a route.

    This decorator checks if the "logged_in" key exists and is set to True
    in the session. If not, it redirects the user to the login page.

    Args:
        func (Callable): The route function to be decorated.

    Returns:
        Callable: The wrapped function that includes the login check.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            # Redirect to the login page if the user is not logged in
            return redirect(url_for("login_page"))
        # Proceed with the original function if logged in
        return func(*args, **kwargs)

    return wrapper

