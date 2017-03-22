# -*- coding: utf-8 -*-
import tokens
from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, request
from weather import Weather
from util import *
from datetime import datetime
import os.path
main = Blueprint("main", __name__)
weather_api_token = tokens.WEATHER_API_TOKEN

ICONS = {"clear-day": "day-sunny", "clear-night": "night-clear", "rain": "rain", "snow": "snow", "sleet": "sleet",
         "wind": "strong-wind", "fog": "fog", "cloudy": "cloudy", "partly-cloudy-day": "day-cloudy",
         "partly-cloudy-night": "night-cloudy"}


@main.context_processor
def inject_now():
    name = None
    hometown = None
    data = get_data_from_file('users.json')
    if data is not None:
        for user in data['users']:
            if user['logged_in']:
                name = user['name']
                hometown = user['hometown']

    return {'now': datetime.utcnow(), 'name': name, 'hometown': hometown}


@main.route("/home")
@main.route("/home/<string:user>")
def home(user=None):
    if user is None:
        return render_template("user_management.html")
    else:
        weather_params = None
        data = get_data_from_file('users.json')
        for u in data['users']:
            if u['name'] == user:
                city = u['hometown']
                if city is not None:
                    weather_params = get_weather(city)
        return render_template("forecast.html", weather=weather_params)


@main.route("/response")
def response():
    return render_template("response.html")


@main.route("/user_management")
def user_management():
    return render_template("user_management.html")


@main.route("/show_users")
def show_users():
    user_list = get_user_list()
    return render_template("show_users.html", users=user_list)


@main.route("/forecast/<string:city>", methods=["GET","POST"])
def forecast(city):
    weather_params = get_weather(city)

    return render_template("forecast.html", city=city, weather=weather_params)


@main.route("/weather")
def weather():
    return "GOOD FUCKING JOB!"


def get_weather(city):
    weather = Weather(weather_api_token)
    cities = get_data_from_file("cities.json")
    cities = cities['cities']
    current_dtime = datetime.now()
    weather_obj = weather.find_weather(city)
    temperature = weather_obj['temperature']
    temperature = (temperature - 32) * 5 / 9
    temperature = "{0:.1f}".format(temperature)
    icon = weather_obj['icon']
    wind_speed = weather_obj['windSpeed']

    return {'City': city, 'Temperature': temperature, 'Windspeed': wind_speed, 'Icon': ICONS[icon]}
