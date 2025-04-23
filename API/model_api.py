from flask import Blueprint, jsonify, request, abort
from config import logger, ML, actions
from common import extract_keypoints
from decorators import login_required
from error_handler import register_error_handlers_api
import numpy as np



model_bp = Blueprint("model", __name__)

register_error_handlers_api(model_bp)


@model_bp.route("/predict/", methods=["POST"])
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
        prediction = {"result": actions[np.argmax(res)], "input": data}
        # logger.info(f"Prediction result: {prediction}")

        return jsonify(prediction), 200

    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        abort(e)  # Internal Server Error
