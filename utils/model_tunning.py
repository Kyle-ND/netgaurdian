import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import joblib

# Load data
print('Loading data...')
maintenance_data = pd.read_csv('./datasets/maintenance_logs.csv')
failure_data = pd.read_csv('./datasets/failure_data.csv')
usage_data = pd.read_csv('./datasets/usage_patterns.csv')
device_data = pd.read_csv('./datasets/device_maintenance_data.csv')

# Merge data
data = pd.merge(maintenance_data, failure_data, on='device_id')
data = pd.merge(data, usage_data, on='device_id')
data = pd.merge(data, device_data, on='device_id')
print('Data loaded and merged successfully.')

# Preprocessing (handle missing values, convert columns to datetime)
data['maintenance_date'] = pd.to_datetime(data['maintenance_date_y'])
data['failure_date'] = pd.to_datetime(data['failure_date_y'])

# Feature engineering
print('Feature engineering...')
data['time_since_last_maintenance'] = (pd.to_datetime('today') - data['maintenance_date']).dt.days
data['average_usage'] = data['traffic_volume_y'] / data['days_in_service_y']
failure_count = failure_data.groupby('device_id')['failure_date'].count().reset_index()
failure_count.columns = ['device_id', 'failure_count']
data = pd.merge(data, failure_count, on='device_id', how='left')
data['failure_count'] = data['failure_count_y'].fillna(0)

# Calculate failure rate per service day
data['failure_rate_per_service_day'] = data['failure_count'] / data['days_in_service_y']
data['failure_rate_per_service_day'] = data['failure_rate_per_service_day'].fillna(0)  # Handle division by zero or NaN


# Define features (X) and target variable (y)
X = data[['time_since_last_maintenance', 'average_usage', 'failure_count']]
y = data['maintenance_required']  # 1 if maintenance is required, 0 if not

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForestClassifier
print('Training model...')


# Instantiate the model
model = RandomForestClassifier(
    n_estimators=300,
    min_samples_split=10,
    min_samples_leaf=2,
    max_features=None,
    max_depth=20,
    bootstrap=True,
    random_state=42)

model.fit(X_train, y_train)


# Evaluate model
print('Evaluating model...')
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')

# Save model to a .pkl file
print('Saving model...')
joblib.dump(model, './models/maintenance_predictor_model_6.pkl')

# Save model to a .joblib file
print('Saving model...')
joblib.dump(model, './models/maintenance_predictor_model_6.joblib')