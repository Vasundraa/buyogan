from flask import Flask, render_template, jsonify
from Adafruit_IO import Client, RequestError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Adafruit IO configuration
ADAFRUIT_IO_KEY = 'aio_jjyD03U0FSWUhw6blzFVXUnzIvBX'
ADAFRUIT_IO_USERNAME = 'gps_location'
FEED_NAME = 'location'

# Create an instance of the Adafruit IO Client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Initialize variables to store latest coordinates
latest_coordinates = {'latitude': None, 'longitude': None}


# Function to fetch coordinates
def fetch_coordinates():
    global latest_coordinates
    try:
        # Retrieve the latest GPS data from Adafruit IO
        gps_data = aio.receive(FEED_NAME)

        # Extract latitude and longitude
        latitude = gps_data.lat
        longitude = gps_data.lon

        # Update latest coordinates
        latest_coordinates = {'latitude': latitude, 'longitude': longitude}

    except RequestError as e:
        print(f'Error fetching data from Adafruit IO: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')


# Route to render map.html
@app.route('/map')
def map():
    return render_template('map.html')


# Route to fetch coordinates
@app.route('/get_coordinates')
def get_coordinates():
    fetch_coordinates()
    return jsonify(latest_coordinates)


if __name__ == '__main__':
    # Fetch initial coordinates
    fetch_coordinates()

    # Start Flask web server
    app.run(debug=True)
