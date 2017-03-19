# -*- coding: utf-8 -*-
import tokens
from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, request
from weather import Weather
from util import *
from datetime import datetime
main = Blueprint("main", __name__)
weather_api_token = tokens.WEATHER_API_TOKEN


@main.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@main.route("/<string:user_name>/home/<string:city>/<string:response>", methods=["GET","POST"])
def home(user_name, city, response):
    if response == 'None':
        response = None
    weather_params = get_weather(city)
    return render_template("forecast.html", user_name=user_name, weather=weather_params, response=response)


@main.route("/<string:user_name>/set_location")
def set_location(user_name):
    return render_template("set_location.html", user_name=user_name)


@main.route("/user_management")
def user_management():
    user_options = ["1.Log in", "2.Create a new user", "3.See the user list", "4.Delete a user", "5.Go back"]

    return render_template("user_management.html", user_options=user_options)


@main.route("/show_users")
def show_users():

    return render_template("show_users.html")

@main.route("/forecast/<string:city>", methods=["GET","POST"])
def forecast(city):
    weather_params = get_weather(city)

    return render_template("forecast.html", city=city, weather=weather_params)


@main.route("/weather")
def weather():
    return "GOOD FUCKING JOB!"


@main.route("/simple_response/<string:response>")
def simple_response(response):
    return render_template("simple_response.html", response=response)


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

    return {'City': city, 'Temperature':temperature, 'Windspeed': wind_speed, 'Icon':icon}
