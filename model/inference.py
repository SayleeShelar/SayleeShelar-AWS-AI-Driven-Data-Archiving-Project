import joblib
import os
import json
import numpy as np

def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, 'model.joblib'))
    return model

def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        return json.loads(request_body)
    raise ValueError(f'Unsupported content type: {request_content_type}')

def predict_fn(input_data, model):
    data = np.array(input_data['data']).reshape(1, -1)
    return model.predict(data)

def output_fn(prediction, response_content_type):
    if response_content_type == 'application/json':
        return json.dumps(prediction.tolist())
    raise ValueError(f'Unsupported content type: {response_content_type}')
