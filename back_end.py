import numpy as np
import tensorflow as tf
import json
import joblib

STATUS_OK = 200
STATUS_UNEXPECTED = 500
STATUS_SERVICE_UNAVAILABLE = 503
model = None
scaler = None



def initialize_backend_model():
    global model, scaler
    # attempt to load model
    try:
        model = tf.keras.models.load_model('telco_churn_model_Bach.keras')
    # if unsuccessful
    except:
        response_body = {
            "status": "Error",
            "message": "Failed to load neural network model during startup."
        }
        return STATUS_UNEXPECTED, json.dumps(response_body)
    
    #attempt to load scaler
    try:
        scaler = joblib.load('minmax_scaler.pkl')
    # if unsuccessful
    except Exception as e:
        print('----------------------------------------')
        print(e)
        response_body = {
            "status": "Error",
            "message": "Model loaded but scaler failed."
        }
        return STATUS_UNEXPECTED, json.dumps(response_body)
    
    response_body = {
        "status": "Success",
        "message": "Neural network model loaded successfully."
    }
    return STATUS_OK, json.dumps(response_body)



def predict_score(request: str):
    
    # if initialize_backend_model failed, or was not called
    if model is None:
        response_body = {
            "status": "ServiceUnavailable",
            "message": "The model is not loaded."
        }
        return STATUS_SERVICE_UNAVAILABLE, json.dumps(response_body)

    # unkown error handling
    try:
        params = np.array([json.loads(request)]).astype('float32')
        #transform numerical data
        params[0][1] = scaler.transform(np.array([[params[0][1]]]))
        params[0][2] = scaler.transform(np.array([[params[0][2]]]))
        params[0][3] = scaler.transform(np.array([[params[0][3]]]))
        #predict
        prediction = model.predict(params)
    except:
        response_body = {
            "status": "Error",
            "message": "An error occurred during prediction processing."
        }
        return STATUS_UNEXPECTED, json.dumps(response_body)

    # success
    response_body = {
        "status": "Success",
        "message": "Prediction calculated.",
        "prediction": float(prediction[0][0])
    }
    return STATUS_OK, json.dumps(response_body)