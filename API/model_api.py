from flask import Blueprint, jsonify, request, abort
from config import logger
from decorators import login_required
from error_handler import register_error_handlers_api

model_bp = Blueprint("model", __name__)

register_error_handlers_api(model_bp)


@model_bp.route("/predict", methods=["POST"])
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
        logger.info(f"Received data: {data}")

        # Here you would typically call your model's prediction function
        # For demonstration, we'll just return the received data
        prediction = {"result": "dummy_prediction", "input": data}
        # logger.info(f"Prediction result: {prediction}")
        raise Exception("Test exception")  # Simulate an error for testing

        return jsonify(prediction), 200

    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        abort(e)  # Internal Server Error
