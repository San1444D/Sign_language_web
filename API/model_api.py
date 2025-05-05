from flask import Blueprint, jsonify, request, abort, Response, stream_with_context
from COMMON.config import logger, ML, actions
from COMMON.decorators import auth_required
from COMMON.error_handler import register_error_handlers_api
from COMMON.tts import SpeechProcessor
from COMMON.common import play_video
import numpy as np



model_bp = Blueprint("model", __name__)
register_error_handlers_api(model_bp)


@model_bp.route("/predict/", methods=["POST"])
@auth_required
def predict():
    """
    Endpoint for making predictions using the model.

    This endpoint accepts a POST request with JSON data containing the input features
    for the model. It returns a JSON response with the prediction result.

    Returns:
        JSON: A JSON response containing the prediction result.
    """
    try:
        data = request.get_json()
        # logger.info(f"Received data: {data}")
        frames = data['frames']

        res = ML.predict(np.expand_dims(frames, axis=0))[0]
        # Here you would typically call your model's prediction function
        # For demonstration, we'll just return the received data
        result = actions[np.argmax(res)]
        
        sp = SpeechProcessor()
        res = {}
        res["result"] = sp.translate(result, data.get("target_language")) if data.get("target_language") else sp.translate(result)
        
        if data.get("speech_request"):
            res["audio_b64"] = sp.text_to_speech(res["result"], data.get("target_language")) if data.get("target_language") else sp.text_to_speech(res["result"])
        # logger.info(f"Prediction result: {prediction}")
        else:
            res["audio_b64"] = None
            
        return jsonify(res), 200

    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        abort(e)  # Internal Server Error

@model_bp.route("/speech-to-action/", methods=["POST"])
@auth_required
def speech_to_action():
    """
    Endpoint for converting speech to action.

    This endpoint accepts a POST request with JSON data containing the input features
    for the model. It returns a JSON response with the prediction result.

    Returns:
        JSON: A JSON response containing the prediction result.
    """
    try:
        data = request.get_json()
        # logger.info(f"Received data: {data}")
        sp = SpeechProcessor()
        
        text, language = sp.speech_to_text(data['audio'])
        if text is None:
            return jsonify({"error": "Failed to transcribe audio"}), 400

        text = sp.translate(text, language) if language else text 

        res = play_video(text)
        if res is None:
            return jsonify({"error": "Failed to play video"}), 400
        
        # res['text'] = text
        # res['language'] = language
        
        return res, 200
    
    except Exception as e:
        logger.error(f"Error in speech_to_action: {e}")
        abort(e)


@model_bp.route("/text-to-action/", methods=["POST"])
@auth_required
def text_to_action():
    """
    Endpoint for converting text to action.
    This endpoint accepts a POST request with JSON data containing the input text.
    It processes the text and returns a JSON response with the action result.
    
    Returns:
        JSON: A JSON response containing the action result.
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text:
            return jsonify({"error": "Missing or empty 'text' in request"}), 400
        
        res = play_video(text)
        if res is None:
            return jsonify({"error": "Failed to play video"}), 400
        
        return res, 200 

    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        abort(e)