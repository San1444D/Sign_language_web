from flask import Blueprint, jsonify, abort
from COMMON.config import logger
from COMMON.decorators import auth_required
from COMMON.tts import SpeechProcessor

sp = SpeechProcessor()

get_api_bp = Blueprint("get_api", __name__)

@get_api_bp.route("/translate/langs/", methods=["GET"])
@auth_required
def get_translate_langs():
    """
    Endpoint for getting the list of supported languages for translation.
    """
    try:
        google = sp.get_google_supported_languages()
        gtts = sp.get_gtts_supported_languages()
        res = {lang: lang_id for lang, lang_id in google.items() if lang_id in gtts}
        return jsonify(res), 200

    except Exception as e:
        logger.error(f"Error in getting supported languages: {e}")
        abort(500)

