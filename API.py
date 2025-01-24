from flask import Flask, request, jsonify
import joblib  # For loading the trained model
import pandas as pd

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
        result = {
            "device_id": data['device_id'],
            "maintenance_required": bool(prediction),
            "confidence": round(prediction_proba, 2)
        }
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)})
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)