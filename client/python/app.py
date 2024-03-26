from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import pickle
import joblib
import os
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the model

# Replace 'model.joblib' with the path to your .joblib file
model = joblib.load(r'client/python/rf_model.pkl')

@app.route('/handle_data', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the data from the POST request.
        data = request.form.to_dict()
        # Convert the dictionary to a numpy array.
        input_data = np.array(list(data.values())).reshape(1, -1)
        # Make a prediction.
        prediction = model.predict(input_data)
        # Return the result as a JSON response.
        return jsonify(prediction=prediction[0], input_data=data)
    return jsonify(message="No data received")

if __name__ == '__main__':
    app.run(debug=True)