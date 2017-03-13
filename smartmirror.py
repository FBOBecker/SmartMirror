try:
    import tokens
except ImportError:
    print("Couldn't import 'token' file. Create it first.")
    import sys
    sys.exit(0)

import os
import json
from datetime import datetime
from user import *
from wit import *
from util import *



from speech import speech

weather_api_token = tokens.WEATHER_API_TOKEN

class Bot:
    def __init__(self):
        self.current_user = None
        self.ai = Wit()
        self.ai.analyze_request('Gochsheim')
        self.weather = ''

    def run(self):
        """
        Bot running
        """

        if os.path.isfile("last_use.json"):

            data = get_data_from_file("last_use.json")
            if data is not None:
                if 'name' in data:
                    self.login(data['name'])
                    print("Welcome back, " + self.current_user.name + "!")
                    self.current_user.show_hobbies()

        else:
            f = open("last_use.json", "w+")
            f.close()

        while True:
            if(self.logged_in()):
                "Hello " + self.current_user.name + "!"
            print("You are in main menu.\nAsk me what I can do.")
            self.update_file()
            command = speech()
            self.action(command)

    def action(self, command):
        """
        Choose next action depending on input
        :param command:
        :return:
        """
        if any(command in w for w in ["hello", "hi"]):
            print("Greetings")
        elif any(command in w for w in ["shutdown bot", "shutdown system", "shut down", "shutdown"]):
            print("Goodbye!")
            exit()
        elif any(command in w for w in ["login", "I want to login", "new account", "user", "new user"]):
            if not self.logged_in():
                self.user_selection()
            else:
                print("You are already logged in as " + self.current_user.name + ". You have to log out first to access " + command + ". Do you want to log out now?")
                command = speech()
                if any(command in w for w in ["yes", "yep", "aye", "yo", "logout", "log out"]):
                    self.logout()
                    self.user_selection()
        elif any(command in w for w in ["hobbies", "show hobbies", "hobby"]):
            if(self.logged_in()):
                self.hobby_selection()
            else:
                print("Log in to view your hobbies.")
        elif any(command in w for w in ["who am I", "Who"]):
            self.who_am_i()
        else:
            print("You said " + command)
        

    def __weather_action(self):
        current_dtime = datetime.now()
        weather_obj = self.weather.find_weather()
        temperature = weather_obj['temperature']
        icon = weather_obj['icon']
        wind_speed = weather_obj['windSpeed']


    def hobby_selection(self):
        print("Do you want to:\n1.View your hobbies?\n2.Add hobbies?\n3.Remove hobbies?\n4.Go back?")

        command = speech()

        print("You said:" + command)

        if any(command in w for w in ["one", "view my hobbies", "view hobbies", "view your hobbies", "view"]):
            self.current_user.show_hobbies()
        elif any(command in w for w in ["two", "add", "add hobbies", "add your hobbies"]):
            self.current_user.add_hobbies()
        elif any(command in w for w in ["three", "remove", "remove hobbies", "remove your hobbies"]):
            self.current_user.remove_hobbies()
        elif any(command in w for w in ["four", "back", "go back"]):
            return




    def user_selection(self):
        in_user_selection = True
        while in_user_selection:
            print("User Selection\nDo you want to:\n1.log in?\n2.Create a new user?\n3.See the user list?\n4.Delete a user?\n5.Go back?")

            command = speech()

            print("You said:" + command)
            if any(command in w for w in ["one", "login", "log in"]):
                in_user_selection = False
                self.login()
            elif any(command in w for w in ["two", "new user", "user", "new", "create new user", "create", "create new"]):
                in_user_selection = False
                self.create_new_user()
            elif any(command in w for w in ["three", "see", "list", "user list", "see the user list"]):
                self.show_users()
                pass
            elif any(command in w for w in ["four", "remove", "remove user", "delete", "delete user"]):
                self.delete_user()
            elif any(command in w for w in ["five", "back", "go back"]):
                in_user_selection = False
                self.run()

    """
    creates a new user in "./users.json"

    """
    def create_new_user(self, new_user=''):

        if not new_user == '':
            self.current_user = User()
            self.current_user.name = new_user
            self.current_user.location = ''


        else:
            correct = False
            while correct == False:
                print("New User creation. Please spell your name for me. To cancel say 'abort' or 'cancel'.")
                command = speech()
                print("You said '" + command + "'. Is that correct?")
                if any(command in w for w in CANCEL_LIST):
                    return
                approval_command = speech()
                if any(approval_command in w for w in APPROVAL_LIST):
                    print("You said "+ approval_command + ".")
                    correct = True
            
            #check if 'users.json'-file alrdy exists
            if not os.path.isfile("users.json"):
                f = open("users.json", "w+")
                user_data = {"users":[]}
                dump_data_to_file(user_data, "users.json")
                f.close()
            #check if name exists in users.json
            else:
                user_data = get_data_from_file("users.json")
                user_list = user_data['users']
                if any(user['name'] == command for user in user_list):
                    print("User already exists... - Choose another name, please.")
                    return self.create_new_user()

            dump_data = get_data_from_file("users.json")

            dump_data["users"].append({"name": command, "location": '', "hobbies": []})
            
            dump_data_to_file(dump_data, "users.json")

            print("User " + command + " successfully created.")
            self.login(command)

    def delete_user(self):
        print("Which user do you want to remove?")
        self.show_users()
        user_list = self.get_user_list()
        if user_list is None or len(user_list) == 0:
            print("There are no users yet.")
        else:
            command = speech()
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
                if command in user_match.keys():
                    user_to_delete = user_match[command]
                else:
                    user_to_delete = command

                user_data = get_data_from_file("users.json")
                user_list = user_data['users']

                item_index = next(index for (index, user) in enumerate(user_list) if user['name'] == user_to_delete)

                approval_command = speech()

                if any(approval_command in w for w in APPROVAL_LIST):
                    del user_list[item_index]

                    user_data['users'] = user_list

                    dump_data_to_file(user_data, "users.json")
                    self.update_file()

    def login(self, user_name=''):
        if not self.current_user is None:
            print("You are already logged in as " + self.current_user.name + ". Log out first.")
        else:
            user_list = self.get_user_list()
            if user_list is None or len(user_list) == 0:
                print("There are no Users to chose from. - Redirecting to User Creation")
                self.create_new_user()
            else:
                if not user_name == '':
                    user_data = get_data_from_file("users.json")
                    for user in user_data['users']:
                        if user['name'] == user_name:
                            self.current_user = User()
                            self.current_user.name = user['name']
                            self.current_user.location = user['location']
                            self.current_user.hobbies = user['hobbies']
                else:
                    while(not(self.logged_in())):
                        print("Select your Profile from the following list of users by saying the Name or Number:")
                        
                        count = 1
                        for user in user_list:
                            print(str(count)+"." + user)
                            count += 1

                        command = speech()
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
                                    self.current_user.location = user['location']
                                    self.current_user.hobbies = user['hobbies']

                            dump_data = {"name": self.current_user.name}

                            dump_data_to_file(dump_data, "last_use.json")
                            print("Hello " + self.current_user.name + "!\nYou are logged in now!")

                self.update_file()




    def logout(self):
        if(self.logged_in()):
            self.current_user = None
            self.update_file()
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
        print(self.get_user_list())


    def get_user_list(self):
        if os.path.isfile("users.json"):
            user_data = get_data_from_file("users.json")
            if not(user_data is None):
                user_list = []
                for user in user_data['users']:
                    user_list.append(user['name'])
                return user_list
        return None
                


    def update_file(self):
        if self.logged_in():
            data = {"name": self.current_user.name}
            dump_data_to_file(data, "last_use.json")
        else:
            if(os.path.isfile("last_use.json")):
                os.remove("last_use.json")



if __name__ == "__main__":
    bot = Bot()
    bot.run()
