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

    if request == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)  # get city2 from the form

        # deal with data somehow
    else:
        return render(request, 'weatherApp/index.html')
