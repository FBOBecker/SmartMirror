import json
import requests
from datetime import datetime



class Weather:
    def find_weather(self):
        loc_obj = self.get_location()

        lat = loc_obj['lat']
        lon = loc_obj['lon']

        weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s" % (self.weather_api_token, lat, lon)
        r = requests.get(weather_req_url)
        weather_json = json.loads(r.text)

        temperature = int(weather_json['currently']['temperature'])

        current_forecast = weather_json['currently']['summary']
        hourly_forecast = weather_json['minutely']['summary']
        daily_forecast = weather_json['hourly']['summary']
        weekly_forecast = weather_json['daily']['summary']
        icon = weather_json['currently']['icon']
        wind_speed = int(weather_json['currently']['windSpeed'])

        return {'temperature': temperature, 'icon': icon, 'windSpeed': wind_speed,
                'current_forecast': current_forecast, 'hourly_forecast': hourly_forecast,
                'daily_forecast': daily_forecast, 'weekly_forecast': weekly_forecast}

    def get_location(self):
        # get location
        location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
        r = requests.get(location_req_url)
        location_obj = json.loads(r.text)

        lat = location_obj['latitude']
        lon = location_obj['longitude']

        return {'lat': lat, 'lon': lon}

    def __weather_action(self, nlu_entities=None):
        current_dtime = datetime.datetime.now()

        weather_obj = self.knowledge.find_weather()
        temperature = weather_obj['temperature']
        icon = weather_obj['icon']
        wind_speed = weather_obj['windSpeed']


weather_api_token = '515b1a5c1216ffa30793e24c4f09b94a'
