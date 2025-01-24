import csv
import requests

# Define the URL of your Flask app
url = 'http://127.0.0.1:5000/predict-maintenance'  # Replace with your actual endpoint

# Read the CSV file
csv_file_path = './datasets/devices_data_100.csv'  # Replace with the path to your CSV file

with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Make a POST request to the Flask app with the row data
        response = requests.post(url, json=row)
        print(f'Status Code: {response.status_code}, Response: {response.json()}')