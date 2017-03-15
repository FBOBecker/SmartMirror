# -*- coding: utf-8 -*-
import tokens
from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, request
from weather import Weather
from util import *
main = Blueprint("main", __name__)
weather_api_token = tokens.WEATHER_API_TOKEN


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

    return render_template("home.html", temp=temperature, wind=wind_speed, city=city)


@main.route("/weather")
def weather():
    return "GOOD FUCKING JOB!"
