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


@main.context_processor
def inject_now():
    name = None
    hometown = None
    today = datetime.today().timetuple()
    date = str(today[2]) + '.' + str(today[1]) + '.' + str(today[0])
    time = str(today[3]) + ':' + str(today[4])
    weekday = WEEKDAYS[today[6]]
    time_icon = None
    if 8 < today[3] < 15:
        time_icon = "sunrise"
    elif 15 < today[3] < 21:
        time_icon = "sunset"
    elif 21 < today[3]:
        time_icon = "moonrise"
        print("Moonrise")
    elif today[3] < 8:
        time_icon = "moonset"
    data = get_data_from_file('users.json')
    if data is not None:
        for user in data['users']:
            if user['logged_in']:
                name = user['name']
                hometown = user['hometown']

    return {'date': date, 'time': time, 'weekday': weekday, 'time_icon':time_icon, 'name': name, 'hometown': hometown}


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


@main.route("/sleep")
def sleep():
    return render_template("sleep.html", name=None)


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
            if key == "temperature" or key == "temperatureMin" or key == "temperatureMax":
                dict[key] = "{0:.1f}".format(((dict[key] - 32) * 5 / 9))
            if key == "icon":
                dict[key] = ICONS[dict[key]]
        dict['weekday'] = WEEKDAYS[dateutil.parser.parse(dict['time']).weekday()]
        dict['hour'] = dateutil.parser.parse(dict['time']).hour

    # print(weather_obj)
    weather_obj[0]['city'] = city
    return weather_obj
