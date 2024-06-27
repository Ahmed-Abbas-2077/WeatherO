import datetime
import requests
from django.shortcuts import render

# Create your views here.


def index(request):

    # API_KEY is stored in a file named API_KEY
    API_KEY = open('../../../API_KEY', 'r').read()

    # q is the query parameter for city name and appid is the API key
    current_weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

    # lat and lon are the latitude and longitude of the city,
    # exclude is the parameter to exclude the current, minutely and hourly weather data, appid is the API key
    forecast_url = 'http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)  # is optional

        # Fetching the weather data and 5-day forecast of the city
        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(
            city1, api_key, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url,
                                                                         forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        # context is a dictionary that contains the data that is to be rendered in the template
        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


# This function fetches the current weather and 5-day forecast of the city (not a route handler)
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):

    # A json response with the city's weather data
    response = requests.get(current_weather_url.format(city, api_key)).json()

    # lat and lon are the latitude and longitude of the city, respectively
    lat, lon = response['coord']['lat'], response['coord']['lon']

    # A json response with the city's 5-day forecast data
    forecast_response = requests.get(
        forecast_url.format(lat, lon, api_key)).json()

    # Extracting the required data from the json responses
    weather_data = {
        'city': city,
        # converting temperature from Kelvin to Celsius. 2 is the number of decimal places
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    daily_forecasts = []
    for daily_data in forecast_response['daily'][:5]:
        daily_forecasts.append({
            # converting timestamp to day. strftime is used to format the date into a readable form
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            # converting temperature from Kelvin to Celsius. 2 is the number of decimal places
            'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
            'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts
