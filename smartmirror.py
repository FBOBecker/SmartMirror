from time import sleep

try:
    import tokens
except ImportError:
    print("Couldn't import 'token' file. Create it first.")
    import sys
    sys.exit(0)

import os
import json
import sys
from datetime import datetime
from user import *
from util import *
from weather import Weather
from speech import write

import requests

from wit import wit

from selenium import webdriver

weather_api_token = tokens.WEATHER_API_TOKEN
wit_token = tokens.WIT_ACCESS_TOKEN


class Bot():
    URL_WIT = 'https://api.wit.ai/message?v=20170319&q={}'
    URL_USER_HOME = "http://localhost/{}/home"
    URL_USER_MANAGEMENT = "http://localhost/user_management"
    URL_FORECAST = "http://localhost/forecast/{}"
    URL_RESPONSE = "http://localhost/response"

    def __init__(self, mode=write):
        super().__init__()
        self.current_user = None
        self.weather = Weather(weather_api_token)
        cities = get_data_from_file("cities.json")
        self.cities = cities['cities']
        self.speech = mode
        self.driver = webdriver.Chrome()

        data = get_data_from_file("last_use.json")
        if data is not None:
            if 'name' in data:
                self.login(data['name'])
                print("Welcome back, " + self.current_user.name + "!")
        else:
            f = open("last_use.json", "w+")
            f.close()
            self.change_url(self.URL_USER_MANAGEMENT)
            self.user_management()

    def run(self):
        """
        Bot running
        """
        while True:
            sleep(0.1)
            try:
                os.remove('response.json')
            except Exception as e:
                print(e)
                pass
            try:
                command = self.speech()
            except Exception as e:
                print(e)
                continue

            self.action(command)

    def action(self, command):
        if self.logged_in():
            name = self.current_user.name
        else:
            name = 'None'

        r = None
        try:
            r = requests.get(self.URL_WIT.format(command), 
                headers={"Authorization": wit_token})
        except Exception as e:
            # did not get the request from wit.ai
            print("REQUEST FAILED")
            self.write_response('Request to wit.ai did not work.')
            self.change_url(self.URL_USER_HOME.format(name))
            return

        if r is not None:
            print(r.text)
            json_resp = json.loads(r.text)
            if 'error' in json_resp:
                print('Authentication with wit.ai failed.')
                self.change_url(self.URL_USER_HOME.format(name))
                return
            intent = self.get_intent(json_resp)
            location = self.get_location(json_resp)

            if intent is not None:
                if intent == 'weather':
                    location = self.get_location(json_resp)
                    if location is not  None:
                        self.change_url(self.URL_FORECAST.format(location))
                    else:
                        self.write_response( "Desired text")
                        self.change_url(self.URL_USER_HOME.format(name))
                        location = self.speech()
                        if location in self.cities:
                            self.write_response()
                            self.change_url(self.URL_USER_HOME.format(name))
                        else:
                            self.write_response('I do not know of this place, sorry!')
                            self.change_url(self.URL_USER_HOME.format(name))
                elif intent == 'hometown':
                    self.set_user_location()
                elif intent == 'logout':
                    self.logout()
                elif intent == 'login':
                    self.write_response("Logintext")
                    self.login()
                elif intent == 'greeting':
                    self.write_response('Hello yourself!')
                    self.change_url(self.URL_USER_HOME.format(name))
                elif intent == 'options':
                    self.use_options()
                elif intent == 'user_creation':
                    self.create_new_user()
                elif intent == 'user_deletion':
                    self.delete_user()
                elif intent == 'user_show':
                    self.show_users()
                elif intent == 'shutdown':
                    exit()
            elif location is not None:
                    self.change_url(self.URL_USER_HOME.format(name))
            else:
                self.response = 'I do not understand the intend of your statement.'
                self.change_url(self.URL_USER_HOME.format(name))
        
    def set_user_location(self):
        """
        TODO: if old_hometown == new_hometown -> print something and exit
        """
        if self.logged_in():
            if self.current_user.hometown is not None:
                print("Your current hometown is '" + self.current_user.hometown + "'")
            self.write_response("Telle me which town to set as your hometown.")
            self.change_url(self.URL_USER_HOME.format(self.current_user.name))
            print('Tell me which town to set as your hometown.')

            command = self.speech()

            if command in self.cities:
                self.current_user.hometown = command
                data = get_data_from_file("users.json")
                for user in data['users']:
                    if user["name"] == self.current_user.name:
                        user['hometown'] = self.current_user.hometown
                dump_data_to_file(data, "users.json")
                self.write_response('Hometown successfully set to ' + self.current_user.hometown + '!')
                self.change_url(self.URL_USER_HOME.format(self.current_user.name))

                print("Set your hometown to '" + self.current_user.hometown + "'.")
            else:
                self.write_response("I may not know that city.")
                self.change_url(self.URL_USER_HOME.format(self.current_user.name))
                print("I may not know that city.")
        else:
            self.write_response("Log in first before setting a hometown.")
            self.change_url(self.URL_USER_HOME.format('None'))

    def use_options(self):
        if self.logged_in():
            self.change_url(self.URL_USER_HOME.format(self.current_user.name, self.current_user.hometown, 
                "You can ask me for the weather, set your hometown, manage your hobbies or log out."))
        else:
            self.user_management()

    def hobby_selection(self):
        print("Do you want to:\n1.View your hobbies?\n2.Add hobbies?\n3.Remove hobbies?\n4.Go back?")

        command = self.speech()

        print("You said:" + command)

        if any(command in w for w in ["one", "view my hobbies", "view hobbies", "view your hobbies", "view"]):
            self.current_user.show_hobbies()
        elif any(command in w for w in ["two", "add", "add hobbies", "add your hobbies"]):
            self.current_user.add_hobbies()
        elif any(command in w for w in ["three", "remove", "remove hobbies", "remove your hobbies"]):
            self.current_user.remove_hobbies()
        elif any(command in w for w in ["four", "back", "go back"]):
            return

    def user_management(self):
        if(self.logged_in()):
            self.write_response("You are already logged in as " + self.current_user.name + ".")
            self.change_url(self.URL_USER_HOME.format(self.current_user.name))
            return
        else:
            self.change_url(self.URL_USER_MANAGEMENT)

    """
    creates a new user in "./users.json"

    """
    def create_new_user(self, new_user=''):

        if not new_user == '':
            self.current_user = User()
            self.current_user.name = new_user
            self.current_user.hometown = ''

        else:
            correct = False
            while not correct:
                self.write_response("New User creation. Please spell your name for me. To cancel say 'abort' or 'cancel'.")
                self.change_url(self.URL_RESPONSE)
                print("New User creation. Please spell your name for me. To cancel say 'abort' or 'cancel'.")
                self.change_url
                command = self.speech()
                print("You said '" + command + "'. Is that correct?")
                self.write_response("You said '" + command + "'. Is that correct?")
                self.change_url(self.URL_RESPONSE)
                if any(command in w for w in CANCEL_LIST):
                    return
                approval_command = self.speech()
                if any(approval_command in w for w in APPROVAL_LIST):
                    print("You said " + approval_command + ".")
                    correct = True
            # check if 'users.json'-file alrdy exists
            if not os.path.isfile("users.json"):
                f = open("users.json", "w+")
                user_data = {"users": []}
                dump_data_to_file(user_data, "users.json")
                f.close()
            # check if name exists in users.json
            else:
                user_data = get_data_from_file("users.json")
                user_list = user_data['users']
                if any(user['name'] == command for user in user_list):
                    print("User already exists... - Choose another name, please.")
                    self.write_response("User already exists... - Choose another name, please.")
                    self.change_url(self.URL_RESPONSE)
                    return self.create_new_user()

            dump_data = get_data_from_file("users.json")

            dump_data["users"].append({"name": command, "hometown": None, "hobbies": None, "logged_in": False})

            dump_data_to_file(dump_data, "users.json")

            print("User " + command + " successfully created.")
            self.write_response("User " + command + " successfully created.")
            self.change_url(self.URL_RESPONSE)
            sleep(3)
            self.login(command)

    def delete_user(self):
        user_list = get_user_list()
        if user_list is None or len(user_list) == 0:
            print("There are no users yet.")
            self.write_response("There are no users yet.")
            self.change_url(self.URL_RESPONSE)
            sleep(3)
            self.write_response(None, True)
            self.change_url(self.URL_USER_MANAGEMENT)
        else:
            print("Which user do you want to remove?")
            self.write_response("Which user do you want to remove?")
            self.show_users()
            command = self.speech()
            print("You said " + command)

            command_list = []
            user_match = {}

            count = 1
            for i in user_list:
                command_list.append(number_conversion(count))
                command_list.append(i)
                user_match[number_conversion(count)] = i
                count += 1

            print("numbers:", command_list)
            print("NAMES:", user_match)
            if any(command in w for w in command_list):
                if command in user_match.keys():
                    user_to_delete = user_match[command]
                else:
                    user_to_delete = command

                user_data = get_data_from_file("users.json")
                user_list = user_data['users']

                item_index = next(index for (index, user) in enumerate(user_list) if user['name'] == user_to_delete)
                
                user_name = user_list[item_index]['name']
                print('Are you sure you want to delete ' + user_name + '?')
                self.write_response('Are you sure you want to delete ' + user_name + '?')
                self.change_url(self.URL_RESPONSE)
                approval_command = self.speech()

                if any(approval_command in w for w in APPROVAL_LIST):
                    del user_list[item_index]

                    if len(user_list) == 0:
                        os.remove('users.json')
                    else:
                        user_data['users'] = user_list
                        dump_data_to_file(user_data, "users.json")

                    print('User ' + user_name + ' deleted!')
                    self.write_response('User ' + user_name + ' deleted!')
                else:
                    self.write_response('Did not delete the user')
                self.change_url(self.URL_USER_MANAGEMENT)

    def login(self, user_name=''):
        if self.current_user is not None:
            print("You are already logged in as " + self.current_user.name + ". Log out first.")
            self.write_response("You are already logged in as " + self.current_user.name + ". Log out first.") 
            self.change_url(self.URL_USER_HOME.format(self.current_user.name))
        else:
            user_list = get_user_list()
            if user_list is None or len(user_list) == 0:
                print("There are no Users to chose from. - Redirecting to User Creation")
                self.write_response("There are no Users to chose from. - Redirecting to User Creation") 
                self.change_url(self.URL_RESPONSE)
                sleep(3)
                self.create_new_user()
            else:
                if not user_name == '':
                    user_data = get_data_from_file("users.json")
                    for user in user_data['users']:
                        if user['name'] == user_name:
                            self.current_user = User()
                            self.current_user.name = user['name']
                            self.current_user.hometown = user['hometown']
                            self.current_user.hobbies = user['hobbies']
                            user['logged_in'] = True

                            dump_data_to_file(user_data, 'users.json')
                else:
                    while(not(self.logged_in())):
                        print("Select your Profile from the following list of users by saying the Name or Number:")
                        self.show_users()

                        command = self.speech()
                        print("You said " + command)

                        command_list = []
                        user_match = {}

                        count = 1
                        for i in user_list:
                            command_list.append(number_conversion(count))
                            command_list.append(i)
                            user_match[number_conversion(count)] = i
                            count += 1

                        if any(command in w for w in command_list):
                            self.current_user = User()
                            if command in user_match.keys():
                                self.current_user.name = user_match[command]
                            else:
                                self.current_user.name = command

                            data = get_data_from_file("users.json")

                            for user in data['users']:
                                if user['name'] == self.current_user.name:
                                    self.current_user.hometown = user['hometown']
                                    self.current_user.hobbies = user['hobbies']
                                    user['logged_in'] = True

                            dump_data = {"name": self.current_user.name}

                            dump_data_to_file(dump_data, "last_use.json")
                            dump_data_to_file(data, 'users.json')
                            print("Hello " + self.current_user.name + "!\nYou are logged in now!")

                
                self.change_url(self.URL_USER_HOME.format(self.current_user.name))

    def logout(self):
        if(self.logged_in()):
            data = get_data_from_file('users.json')
            for user in data['users']:
                if user['logged_in']:
                    user['logged_in'] = False
            dump_data_to_file(data, 'users.json')
            self.current_user = None
            
            self.user_management()
        else:
            print("You are not logged in.")

    def logged_in(self):
        if self.current_user is None:
            return False
        else:
            return True

    def who_am_i(self):
        if (self.logged_in()):
            print("You are " + self.current_user.name + ".")
        else:
            print("How would I know such a thing? You are not logged in...")

    def show_users(self):
        print(get_user_list())
        self.change_url("http://localhost/show_users")

    def update_file(self):
        if self.logged_in():
            data = {"name": self.current_user.name}
            dump_data_to_file(data, "last_use.json")
        else:
            if(os.path.isfile("last_use.json")):
                os.remove("last_use.json")

    def get_intent(self, json_wit):
        intent = None
        if 'entities' in json_wit and 'intent' in json_wit['entities']:
            entities = json_wit['entities']
            intent = entities['intent'][0]['value']
        return intent

    def get_location(self, json_wit):
        location = None
        if 'entities' in json_wit and 'location' in json_wit['entities']:
            entities = json_wit['entities']
            location = entities['location'][0]['value']
        return location

    def change_url(self, url):
        self.driver.get(url)

    def close_browser(self):
        self.driver.close()

    def write_response(self, response, NORESPONSE=False):
        if NORESPONSE:
            os.remove('response.json')
        else:
            data = {'response': response}
            dump_data_to_file(data, 'response.json')