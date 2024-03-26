from flask import escape
import requests
import sqlite3
from google.cloud import storage

def get_weather(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'date1' in request_json and 'date2' in request_json:
        date1 = escape(request_json['date1'])
        date2 = escape(request_json['date2'])
    elif request_args and 'date1' in request_args and 'date2' in request_args:
        date1 = escape(request_args['date1'])
        date2 = escape(request_args['date2'])
    else:
        return 'Missing dates'
    
    latitude = "42.3314"
    longitude = "-83.0458"
    response = requests.get(f'https://api.weather.gov/points/{latitude},{longitude}/observations?start={date1}&end={date2}')

    return response.json()

def update_sqlite_database(df_forecast_relevant):
    conn = sqlite3.connect('forecast_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_forecast (
            Date DATE,
            TimeDay TEXT,
            AVG_TEMP INTEGER,
            shortForecast TEXT,
            AVG_DEWPT REAL,
            AVG_RELHUM REAL,
            AVG_WSPD TEXT,
            PRIMARY KEY (Date, TimeDay)
        )
    ''')

    for _, row in df_forecast_relevant.iterrows():
        cursor.execute('''
            INSERT OR REPLACE INTO weather_forecast 
            (Date, TimeDay, AVG_TEMP, shortForecast, AVG_DEWPT, AVG_RELHUM, AVG_WSPD)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (row.Date, row.TimeDay, row.AVG_TEMP, row.shortForecast, row.AVG_DEWPT, row.AVG_RELHUM, row.AVG_WSPD))

    conn.commit()
    conn.close()

df_forecast_relevant = get_weather()
update_sqlite_database(df_forecast_relevant)
print("Database updated with the latest forecast data.")

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

# Replace with your bucket name, SQLite DB file path and destination file name
upload_blob('your-bucket-name', 'path/to/your/database.db', 'destination-name.db')