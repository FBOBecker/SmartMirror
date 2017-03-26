import json
import requests
from datetime import datetime
from util import dump_data_to_file
from tokens import GOOGLE_MAPS_TOKEN
from cache import *


class Weather:
    LOCATION_URL = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key=" + GOOGLE_MAPS_TOKEN
    WEATHER_URL = "https://api.darksky.net/forecast/{}/{{}},{{}}"

    def __init__(self, weather_api_token):
        self.weather_url = self.WEATHER_URL.format(weather_api_token)

    def find_weather(self, city, time):
        loc_obj = self.get_coordinates(city)

        lat = loc_obj['lat']
        lng = loc_obj['lng']

        key = 'weather' + city

        if get_cache_entry(key) is not None:
            weather_json = get_cache_entry(key)
        else:
            weather_req_url = self.weather_url.format(lat, lng)
            r = requests.get(weather_req_url)
            weather_json = json.loads(r.text)
            dump_data_to_file(weather_json, "weather.json")
            set_cache_entry(key, weather_json)

        if time == 0:
            return [weather_json['currently']]
        elif time == 1:
            weather = [weather_json['currently']] + weather_json['hourly']['data']
            return weather
        else:
            return weather_json['daily']['data']

    def get_coordinates(self, city='Berlin'):
        key = 'loc' + city
        if get_cache_entry(key) is not None:
            location_obj = get_cache_entry(key)
        else:
            location_req_url = self.LOCATION_URL.format(city)
            r = requests.get(location_req_url)
            location_obj = json.loads(r.text)
            dump_data_to_file(location_obj, "location.json")
            set_cache_entry(key, location_obj)

        lat = location_obj['results'][0]['geometry']['location']['lat']
        lng = location_obj['results'][0]['geometry']['location']['lng']

        return {'lat': lat, 'lng': lng}
