import json
import requests
from datetime import datetime
from util import dump_data_to_file
from tokens import GOOGLE_MAPS_TOKEN


class Weather:
    LOCATION_URL = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key=" + GOOGLE_MAPS_TOKEN
    WEATHER_URL = "https://api.darksky.net/forecast/{}/{{}},{{}}"

    def __init__(self, weather_api_token):
        self.weather_url = self.WEATHER_URL.format(weather_api_token)

    def find_weather(self, city):
        loc_obj = self.get_coordinates(city)

        lat = loc_obj['lat']
        lng = loc_obj['lng']

        weather_req_url = self.weather_url.format(lat, lng)
        r = requests.get(weather_req_url)
        weather_json = json.loads(r.text)

        print(weather_json.keys())
        dump_data_to_file(weather_json, "weather.json")

        temperature = int(weather_json['currently']['temperature'])

        current_forecast = weather_json['currently']['summary']
        hourly_forecast = weather_json['hourly']['summary']
        daily_forecast = weather_json['daily']['summary']
        icon = weather_json['currently']['icon']
        wind_speed = int(weather_json['currently']['windSpeed'])

        return {'temperature': temperature, 'icon': icon, 'windSpeed': wind_speed,
                'current_forecast': current_forecast, 'hourly_forecast': hourly_forecast,
                'daily_forecast': daily_forecast}

    def get_coordinates(self, city='Berlin'):
        # get location
        location_req_url = self.LOCATION_URL.format(city)
        r = requests.get(location_req_url)
        location_obj = json.loads(r.text)

        dump_data_to_file(location_obj, "location.json")

        lat = location_obj['results'][0]['geometry']['location']['lat']
        lng = location_obj['results'][0]['geometry']['location']['lng']
        print(lat, lng)

        return {'lat': lat, 'lng': lng}

    def get_ip(self):
        ip_url = "http://jsonip.com/"
        req = requests.get(ip_url)
        ip_json = json.loads(req.text)
        return ip_json['ip']
