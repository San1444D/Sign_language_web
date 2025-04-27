from flask import Flask
from flask_cors import CORS
from datetime import timedelta
from dotenv import load_dotenv
from COMMON.config import APP_SECRET, logger

load_dotenv()



app = Flask(__name__, static_folder=r"./src/static", template_folder=r"./src/templates")
app.secret_key = APP_SECRET  # Set a secret key for session management

CORS(app)

# Configure session cookie settings
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Adjust session expiration as needed
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Can be 'Strict', 'Lax', or 'None'



from API import api as api_blueprint
from WEB import web as web_blueprint

app.register_blueprint(api_blueprint, url_prefix="/api")
app.register_blueprint(web_blueprint, url_prefix="/")

from COMMON.error_handler import register_error_handlers_web
register_error_handlers_web(app)


if __name__ == '__main__':
    app.run(debug=True)