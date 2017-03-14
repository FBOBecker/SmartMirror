from json import load, dump
from json.decoder import JSONDecodeError


number_conversion = {
    1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
    6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
    11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
    15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen'
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
    except (IOError, JSONDecodeError):
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
