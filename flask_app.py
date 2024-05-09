from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderInsufficientPrivileges
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from geopy.exc import GeocoderUnavailable

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']

    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)       
        print(location)

        
    except GeocoderUnavailable as e:
        error_message = "Geocoder service is currently unavailable. Please try again later."
        return render_template('index.html', error=error_message)
    
    except Exception as e:
        error_message = "An unexpected error occurred. Please try again later."
        return render_template('index.html', error=error_message)

    if not location:
        error_message = "Invalid city name. Please enter a valid city."
        return render_template('index.html', error=error_message)


    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")

    api = "https://api.openweathermap.org/data/2.5/weather?q="+ city + "&appid=54c364373b2349f70f30533832b3713f"

    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    description = json_data['weather'][0]['description']
    temp = int(json_data['main']['temp'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']

    weather_data = {
        'city': city,
        'current_time': current_time,
        'temp': temp,
        'condition': condition,
        'feels_like': temp,
        'wind': wind,
        'humidity': humidity,
        'description': description,
        'pressure': pressure
    }
    
    print(weather_data)

    return render_template('weather.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
