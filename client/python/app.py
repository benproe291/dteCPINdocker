from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import pickle
import joblib
import os
import matplotlib.pyplot as plt
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from flask_cors import CORS
from datetime import timedelta
import seaborn as sns
import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

app = Flask(__name__)
# CORS(app)

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
        # Return the result as a JSON response.dump
        return jsonify(prediction=prediction[0], input_data=data)
    return jsonify(message="No data received")

@app.route('/upload', methods=['GET', 'POST'])
def another_route():
    if request.method == 'POST':
        # Handle POST request here
        data = request.files['csvFile']
        #convert 'READING_START_DATE' to datetime
        data['READING_START_DATE'] = pd.to_datetime(data['READING_START_DATE'])

        #extract year, month, day, and day of week
        data['DAY_OF_WEEK'] = data['READING_START_DATE'].dt.dayofweek
        data['MONTH'] = data['READING_START_DATE'].dt.month
        data['YEAR'] = data['READING_START_DATE'].dt.year
        #create calendar
        cal = calendar()
        holidays = cal.holidays(start=data['READING_START_DATE'].min(), end=data['READING_START_DATE'].max())
        #col to indicate if date is a holiday
        data['IS_HOLIDAY'] = data['READING_START_DATE'].isin(holidays).astype(int)

        predictions = []
        for index, row in data.iterrows():
            # Convert the row to a numpy array and reshape it
            input_data = np.array(row.values).reshape(1, -1)
            # Make a prediction
            prediction = model.predict(input_data)
            # Append the prediction to the list
            predictions.append(prediction[0])

        # Add the predictions as a new column in the DataFrame
        data['prediction'] = predictions

        # Save the DataFrame to a new CSV file
        outputFile = data.to_csv('short/predictions.csv', index=False)

        #temp vs. energy consumption
        plt.figure(figsize=(10, 6))
        ax = sns.scatterplot(x='AVG_TEMP', y='sum(TOTAL_KWH)', hue='IsHoliday', data=data)
        plt.title('Temperature vs. Energy Consumption')
        plt.xlabel('Average Temperature (°F)')
        plt.ylabel('Energy Consumption (kWh)')
        y_formatter = FuncFormatter(lambda x, p: format(int(x), ','))
        ax.yaxis.set_major_formatter(y_formatter)
        plt.savefig('short/tempEnergy.png', dpi=300)

        #plotting energy consumption of holiday vs non-holiday
        avg_energy_by_holiday = data.groupby('IsHoliday')['sum(TOTAL_KWH)'].mean().reset_index()

        #t-test
        holiday_energy = data[data['IsHoliday']]['sum(TOTAL_KWH)']
        non_holiday_energy = data[~data['IsHoliday']]['sum(TOTAL_KWH)']
        t_stat, p_value = ttest_ind(holiday_energy, non_holiday_energy)

        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x='IsHoliday', y='sum(TOTAL_KWH)', data=avg_energy_by_holiday)
        plt.title('Average Energy Consumption: Holiday vs. Non-Holiday')
        plt.xlabel('Is Holiday')
        plt.ylabel('Average Energy Consumption (kWh)')
        plt.xticks([0, 1], ['Non-Holiday', 'Holiday'])
        y_formatter = FuncFormatter(lambda x, p: format(int(x), ','))
        ax.yaxis.set_major_formatter(y_formatter)
        plt.savefig('short/avgEnergyHoliday.png', dpi=300)

        #plotting the energy consumption by temperature category
        bins = [0, 32, 60, 80, 100]
        labels = ['Cold', 'Cool', 'Warm', 'Hot']

        data['Temp_Category'] = pd.cut(data['AVG_TEMP'], bins=bins, labels=labels)

        plt.figure(figsize=(10, 6))
        ax = sns.boxplot(x='Temp_Category', y='sum(TOTAL_KWH)', data=data)
        plt.title('Energy Consumption by Temperature Category')
        plt.xlabel('Temperature Category')
        plt.ylabel('Energy Consumption (kWh)')
        y_formatter = FuncFormatter(lambda x, p: format(int(x), ','))
        ax.yaxis.set_major_formatter(y_formatter)
        plt.savefig('short/tempBinsConsumption.png', dpi=300)

        #plotting wind speed vs. energy consumption
        bins = [data['AVG_WSPD'].min(), 5, 15, 25, data['AVG_WSPD'].max()]
        labels = ['Calm', 'Breezy', 'Windy', 'Very Windy']
        data['Wind_Category'] = pd.cut(data['AVG_WSPD'], bins=bins, labels=labels)

        plt.figure(figsize=(10, 6))
        ax = sns.boxplot(x='Wind_Category', y='sum(TOTAL_KWH)', data=data)
        plt.title('Energy Consumption by Wind Speed Category')
        plt.xlabel('Wind Speed Category')
        plt.ylabel('Energy Consumption (kWh)')
        y_formatter = FuncFormatter(lambda x, p: format(int(x), ','))
        ax.yaxis.set_major_formatter(y_formatter)
        plt.savefig('short/windSpdEnergy.png', dpi=300)

        #plot holiday vs. surrounding days vs. regular days
        data['Day_Before_Holiday'] = data['READING_START_DATE'].isin(holidays - pd.Timedelta(days=1))
        data['Day_After_Holiday'] = data['READING_START_DATE'].isin(holidays + pd.Timedelta(days=1))

        plt.figure(figsize=(12, 8))
        data['Period'] = np.where(data['IsHoliday'], 'Holiday', np.where(data['Day_Before_Holiday'], 'Day Before Holiday', np.where(data['Day_After_Holiday'], 'Day After Holiday', 'Regular Day')))
        ax = sns.boxplot(x='Period', y='sum(TOTAL_KWH)', data=data)
        plt.title('Energy Consumption: Holiday vs. Surrounding Days vs. Regular Days')
        plt.xlabel('Period')
        plt.ylabel('Energy Consumption (kWh)')
        plt.xticks(rotation=45)
        y_formatter = FuncFormatter(lambda x, p: format(int(x), ','))
        ax.yaxis.set_major_formatter(y_formatter)
        plt.savefig('short/holidayDepression.png', dpi=300)

        #energy consumption vs. temperature
        plt.figure(figsize=(12, 6))
        ax = sns.regplot(x='AVG_TEMP', y='sum(TOTAL_KWH)', data=data, scatter_kws={'alpha':0.5}, line_kws={'color': 'red'})
        plt.title('Effect of Temperature on Energy Consumption')
        plt.xlabel('Average Daily Temperature (°F)')
        plt.ylabel('Daily Energy Consumption (kWh)')
        y_formatter = FuncFormatter(lambda x, p: format(int(x), ','))
        ax.yaxis.set_major_formatter(y_formatter)
        plt.savefig('short/energyTemp.png', dpi=300)

        return jsonify(message=request.form.to_dict()), outputFile

if __name__ == '__main__':
    app.run(debug=True)