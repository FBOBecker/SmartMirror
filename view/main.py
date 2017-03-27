# -*- coding: utf-8 -*-
import tokens
from flask import Blueprint, render_template
from weather import Weather
from util import *
from datetime import datetime, timedelta, timezone
import dateutil.parser
main = Blueprint("main", __name__)
weather_api_token = tokens.WEATHER_API_TOKEN

ICONS = {"clear-day": "day-sunny", "clear-night": "night-clear", "rain": "rain", "snow": "snow", "sleet": "sleet",
         "wind": "strong-wind", "fog": "fog", "cloudy": "cloudy", "partly-cloudy-day": "day-cloudy",
         "partly-cloudy-night": "night-cloudy"}

WEEKDAYS = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

LETTERS = {"one": "a", "two": "b", "three": "c", "4": "d", "5": "e", "6": "f", "7": "g", "8": "h",
                  "9": "i", "10": "j", "11": "k", "12": "l", "13": "m", "14": "n", "15": "o", "16": "p",
                  "17": "q", "18": "r", "19": "s", "20": "t", "21": "u", "22": "v", "23": "w", "24": "x",
                  "25": "y", "26": "z"}


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


@main.route("/home/")
@main.route("/home/<string:date_time>/<string:user>")
def home(date_time=0, user=None):
    if user is None:
        return render_template("user_management.html")
    else:
        weather_params = None
        data = get_data_from_file('users.json')
        for u in data['users']:
            if u['name'] == user:
                city = u['hometown']
                if city is not None:
                    weather_params = get_weather(city, date_time)
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


@main.route("/forecast/<string:city>/<string:date_time>")
def forecast(city, date_time):
    weather_params = get_weather(city, date_time)
    return render_template("forecast.html", weather=weather_params)


@main.route("/location/<string:url>/<string:t_type>")
def location(url, t_type):
    return render_template("location.html", url=url, type=t_type)


@main.route("/spell/")
@main.route("/spell/<string:word>")
def spell(word=""):
    return render_template("spell.html", word=word, letter=LETTERS)


def get_weather(city, date_time=0):
    if date_time == '0' or date_time == 'None':
        date_time = 0

    if date_time != 0:
        date_time = dateutil.parser.parse(date_time)
        time_dif = abs((date_time - datetime.now(timezone.utc)).total_seconds())
        if time_dif < timedelta(hours=1).total_seconds():
            date_time = 0
        elif time_dif < timedelta(hours=12).total_seconds():
            date_time = 1
        else:
            date_time = 2

    weather = Weather(weather_api_token)
    weather_obj = weather.find_weather(city, date_time)

    for dict in weather_obj:
        for key, value in dict.items():
            if key == "time":
                dict[key] = datetime.fromtimestamp(int(dict[key])).strftime('%Y-%m-%d %H:%M:%S')
                print(type(dict[key]))
            if key == "temperature" or key == "temperatureMin" or key == "temperatureMax":
                dict[key] = "{0:.1f}".format(((dict[key] - 32) * 5 / 9))
            if key == "icon":
                dict[key] = ICONS[dict[key]]
        dict['weekday'] = WEEKDAYS[dateutil.parser.parse(dict['time']).weekday()]
        dict['hour'] = dateutil.parser.parse(dict['time']).hour

    print(weather_obj)
    weather_obj[0]['city'] = city
    return weather_obj
