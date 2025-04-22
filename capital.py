#Jackson Haiz
#Used chatgpt as aid in brainstorming, particularly with the usage of the pytz package

from flask import Flask, jsonify, request
import pytz
from datetime import datetime
import pytz

app = Flask(__name__)

# Dictionary of capitals and their timezones;
cities_timezones = {
    "London": "Europe/London",
    "New York": "America/New_York",
    "Tokyo": "Asia/Tokyo",
    "Paris": "Europe/Paris",
    "Sydney": "Australia/Sydney",
    "Berlin": "Europe/Berlin",
    "Los Angeles": "America/Los_Angeles",
    "Moscow": "Europe/Moscow",
    "Dubai": "Asia/Dubai",
    "Washington D.C": "America/New_York",
    "Charlottesville": "America/New_York" #Not a capital, but I wanted to add it :)
}

API_TOKEN = "supersecrettoken123"  # Your API Token


# Token check decorator
def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401

    decorator.__name__ = f.__name__
    return decorator


@app.route('/api/get-time', methods=['GET'])
@token_required
#Function that retrieves time, will be used in jsonify return function
def get_time():
    city = request.args.get('city')

    if not city or city not in cities_timezones:
        return jsonify({"error": "City not found in the database"}), 404

    # Get the timezone of the city
    timezone = pytz.timezone(cities_timezones[city])

    # Get the current time in the city timezone
    city_time = datetime.now(timezone)
    utc_offset = city_time.utcoffset().total_seconds() / 3600  # in hours

    # Return the current time and UTC offset
    return jsonify({
        "city": city,
        "current_time": city_time.strftime("%Y-%m-%d %H:%M:%S"),
        "utc_offset": utc_offset
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)