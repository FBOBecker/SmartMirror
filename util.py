import os
from json import load, dump
try:
    from json.decoder import JSONDecodeError
except(ImportError):
    from simplejson.decoder import JSONDecodeError

number_conversion = {
    1: 'one', 2: 'two', 3: 'three'
}.get


def get_data_from_file(path):
    """
    Methode um die jsondata eines files zu bekommen
    returns: None if file is empty
                dictionary else
    """
    try:
        with open(path) as f:
            return load(f)
    except (IOError, JSONDecodeError, ValueError):
        return None


# dump data to in jsonformat to jsonfile
def dump_data_to_file(data, path):
    with open(path, "w+") as f:
        dump(data, f, indent=4)


def is_json(file):
    try:
        json_object = load(file)
    except ValueError:
        print('invalid json')
        return False
    return True


def get_user_list():
    if os.path.isfile("users.json"):
        user_data = get_data_from_file("users.json")
        if not(user_data is None):
            user_list = []
            for user in user_data['users']:
                user_list.append(user['name'])
            return user_list
    return None
