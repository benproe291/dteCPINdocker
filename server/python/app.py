from flask import Flask, request, render_template
import pickle
import numpy as np
import pickle

app = Flask(__name__)

# Load the model
from joblib import load

# Replace 'model.joblib' with the path to your .joblib file
model = load('rf.joblib')

@app.route('/handle_data', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the data from the POST request.
        data = request.form.to_dict()
        # Convert the dictionary to a numpy array.
        input_data = np.array(list(data.values())).reshape(1, -1)
        # Make a prediction.
        prediction = model.predict(input_data)
        # Return the result.
        return render_template('index.html', prediction=prediction[0])
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)