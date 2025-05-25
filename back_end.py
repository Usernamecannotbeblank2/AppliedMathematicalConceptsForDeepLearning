import numpy as np
import tensorflow as tf
import json

STATUS_OK = 200
STATUS_UNEXPECTED = 500
STATUS_BAD_REQUEST = 400
model = None



def initialize_backend_model():
    global model
    # attempt to load model
    try:
        model = tf.keras.models.load_model('telco_churn_model_Bach.keras')
        response_body = {
            "status": "success",
            "message": "Neural network model loaded successfully."
        }
        return STATUS_OK, json.dumps(response_body)
    
    # if unsuccessful
    except:
        response_body = {
            "status": "error",
            "message": "Failed to load neural network model during startup."
        }
        return STATUS_UNEXPECTED, json.dumps(response_body)



def predict_score(request: str):
    # if initialize_backend_model failed, or was not called
    if model is None:
        response_body = {
            "status": "error",
            "message": "Service unavailable: The model is not loaded."
        }
        return STATUS_UNEXPECTED, json.dumps(response_body)

    # unkown error handling
    try:
        params = np.array([json.loads(request)]).astype('float32')
        prediction = model.predict(params)
    except:
        response_body = {
            "status": "error",
            "message": "Model failed to predict. Shape may be incorrect."
        }
        return STATUS_UNEXPECTED, json.dumps(response_body)

    # success
    response_body = {
        "status": "success",
        "message": "Prediction calculated.",
        "prediction": float(prediction[0][0])
    }
    return STATUS_OK, json.dumps(response_body)