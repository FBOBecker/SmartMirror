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


@main.route("/")
def index():
    return "Hallo!"


@main.route("/forecast/<string:city>")
def forecast(city):
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

    weather_params = [('City',city), ('Temperature',temperature), ('Windspeed',wind_speed), ('Icon',icon)]

    return render_template("home.html", city=city, temperature=temperature, weather=weather_params)


@main.route("/weather")
def weather():
    return "GOOD FUCKING JOB!"
