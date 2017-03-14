import os
import json
from speech import speech
from util import *

__all__ = ['APPROVAL_LIST', 'CANCEL_LIST', 'DECLINE_LIST', 'User']

user_dir = os.path.relpath("./users/", ".")

APPROVAL_LIST = ["yes", "yep", "si", "aye", "yo"]
CANCEL_LIST = ["cancel", "abort", "stop"]
DECLINE_LIST = ["no", "nope"]


class User:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', '')
        self.location = kwargs.get('location', '')
        self.hobbies = kwargs.get('hobbies', [])

    @property
    def hobby_list(self) -> list:
        """
        :rtype: List[dict]
        """
        user_data = get_data_from_file("users.json")

        for user in user_data['users']:
            if self.name == user.get('name'):
                hobby_data = user.get('hobbies')

        return hobby_data

    def has_hobbies(self):
        hobby_list = self.hobby_list
        if len(hobby_list) > 0:
            return hobby_list
        else:
            return None

    def show_hobbies(self):
        hobbies = self.has_hobbies()
        if not(hobbies is None):
            count = 1
            for hobby in hobbies:
                print(str(count) + ". " + hobby.get('name'))
                count += 1
        else:
            print("You ain't got no hobbies, biatch!")

    def add_hobbies(self):
        print("Which hobby would you like to add?")
        in_loop = True
        while in_loop:
            hobby = speech()
            print("You said '" + hobby + "'. Is that correct?")
            command = speech()
            if (any(command in w for w in APPROVAL_LIST)):

                hobby_list = self.hobby_list
                hobby_list.append({"name": hobby})

                user_data = get_data_from_file("users.json")
                for user in user_data['users']:
                    if(user['name'] == self.name):
                        user['hobbies'] = hobby_list
                        dump_data_to_file(user_data, "users.json")

                in_loop = False

            elif (any(command in w for w in CANCEL_LIST)):
                in_loop = False

    def remove_hobbies(self):
        hobbies = self.has_hobbies()
        if hobbies is None:
            print("You don't have any hobbies.")
        else:
            in_loop = True
            while in_loop:
                print("Which hobby do you want to remove? - State the hobby or its number.")
                self.show_hobbies()

                command_list = []
                hobby_match = {}

                count = 1
                for hobby in hobbies:
                    command_list.append(number_conversion(count))
                    command_list.append(hobby.get('name'))
                    hobby_match[number_conversion(count)] = hobby.get('name')
                    count += 1

                command = speech()

                if any(command in w for w in command_list):
                    if command in hobby_match.keys():
                        hobby_to_remove = hobby_match[command]
                    else:
                        hobby_to_remove = command

                    waiting_for_approval = True
                    while waiting_for_approval:
                        print("Do you really want to remove '" + hobby_to_remove + "' from your hobbies?")

                        approval_command = speech()
                        CANCEL_LIST.extend(DECLINE_LIST)

                        if any(approval_command in w for w in APPROVAL_LIST):
                            item_index = next(i for i, hobby in enumerate(hobbies) if hobby['name'] == hobby_to_remove)
                            del hobbies[item_index]

                            user_data = get_data_from_file("users.json")
                            for user in user_data['users']:
                                if(self.name == user['name']):
                                    user['hobbies'] = hobbies

                            dump_data_to_file(user_data, "users.json")

                            print("Your updated hobbies:")
                            self.show_hobbies()
                            waiting_for_approval = False
                            in_loop = False

                        elif any(approval_command in w for w in CANCEL_LIST):
                            waiting_for_approval = False

                elif any(command in w for w in CANCEL_LIST):
                    print("Cancelled hobby deletion - going back to main menu")
                    return

                else:
                    print("What you said didn't match any of your hobbies."
                          "Try again; to cancel use a word of the CANCEL_LIST.")
