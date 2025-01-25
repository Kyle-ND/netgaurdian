from flask import Flask, request, jsonify
from utils.alert_consumer import send_ntfy_notification
import joblib  # For loading the trained model
import pandas as pd
from utils.get_health import get_health
from utils.get_devices import get_devices

app = Flask(__name__)

model = joblib.load('./models/maintenance_predictor_model_5.pkl')  # Load the trained model

@app.route('/predict-maintenance', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        df = pd.DataFrame([data])
        processed_data = df[['time_since_last_maintenance', 'average_usage', 'failure_count']]
        prediction = model.predict(processed_data)[0]
        prediction_proba = model.predict_proba(processed_data).max()
        if prediction:
            send_ntfy_notification(f"Device {data['device_id']} requires maintenance.")
            
        result = {
            "device_id": data['device_id'],
            "maintenance_required": bool(prediction),
            "confidence": round(prediction_proba, 2)
        }
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/network-health', methods=['GET'])
def network_health():
    try:
        response = get_health()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": e}), 500

@app.route('/devices', methods=['GET'])
def devices():
    try:
        response = get_devices()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True,host='0.0.0.0')