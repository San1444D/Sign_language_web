from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import json, os
import logging

try:
    # Create a logger
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)  # Set the logging level for the logger

    # Create a directory for logs if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Create a TimedRotatingFileHandler
    handler = TimedRotatingFileHandler(
        "logs/app.log",  # File path
        when="M",  # Rotate every (S - Seconds, M - Minutes, H - Hours, D - Days)
        interval=30,  # Every 10 seconds
        backupCount=24,  # Keep last 24 log files
        encoding="utf-8",  # Encoding for the log file
        delay=False,  # Don't delay file creation until the first log message
    )

    # Create a formatter and set it for the handler
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    # Ensure the handler appends logs (default behavior)
    handler.mode = "a"  # 'a' stands for append mode

    # Add the handler to the logger
    logger.addHandler(handler)

    # Optional: Add a console handler for debugging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

except Exception as e:
    print(f"Logger setup error: {e}")

APP_SECRET = None
SESSION_TIME = None

try:
    if not os.path.exists("config.json"):
        raise FileNotFoundError
    try:
        with open("config.json", "r") as file:
            config_json = json.load(file)
            logger.info("config.json loaded")

            APP_SECRET = config_json["Flask"]["SECRET_KEY"]
            SESSION_TIME = config_json["Flask"]["SESSION_TIMEOUT"]
    except PermissionError:
        logger.error("Permission denied while accessing config.json")
    except json.JSONDecodeError:
        logger.error("Malformed JSON in config.json")
    except Exception as e:
        logger.error(f"Unexpected error while loading config.json: {e}")

except FileNotFoundError:
    logger.error("config.json is not found")
except Exception as e:
    logger.error(f"Error loading config.json: {e}")


try:
    from firebase_admin import credentials, firestore, initialize_app

    # Firebase Admin SDK setup
    cred = credentials.Certificate("firebase-auth.json")
    initialize_app(cred)
    db = firestore.client()
    logger.info("Firebase Admin SDK initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing Firebase Admin SDK: {e}")
    