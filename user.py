import os
import json
from speech import speech


user_dir = os.path.relpath("./users/",".")

approval_list = ["yes", "yep", "si", "aye", "yo"]
cancel_list = ["cancel", "abort", "stop"]
decline_list = ["no", "nope"]


class User:
	def __init__(self,*args, **kwargs):
		self.name = kwargs.get('name', '')
		self.location = kwargs.get('location','')
		self.hobbies = kwargs.get('hobbies', [])


	"""
	returns [] with {} entries

	"""
	def get_hobby_list(self):

		user_data = get_data_from_file("users.json")

		for user in user_data['users']:
			if self.name == user.get('name'):
				hobby_data = user.get('hobbies')

		return hobby_data


	def has_hobbies(self):
		hobby_list = self.get_hobby_list()
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
			if (any(command in w for w in approval_list)):

				hobby_list = self.get_hobby_list()
				hobby_list.append({"name": hobby})

				user_data = get_data_from_file("users.json")
				for user in user_data['users']:
					if(user['name'] == self.name):
						user['hobbies'] = hobby_list
						dump_data_to_file(user_data, "users.json")
					
				in_loop = False

			elif (any(command in w for w in cancel_list)):
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
						print("Do you really want to remove '" +  hobby_to_remove + "' from your hobbies?")

						approval_command = speech()
						cancel_list.extend(decline_list)

						if any(approval_command in w for w in approval_list):
							item_index = next(index for (index, hobby) in enumerate(hobbies) if hobby['name'] == hobby_to_remove)
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

						elif any(approval_command in w for w in cancel_list):
							waiting_for_approval = False


				elif any(command in w for w in cancel_list):
					print("Cancelled hobby deletion - going back to main menu")
					return

				else:
					print("What you said didn't match any of your hobbies. Try again; to cancel use a word of the cancel_list.")



def number_conversion(number):
	num2words = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', \
				6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', \
				11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', \
				15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen'}
		
	return num2words[number]


"""
Methode um die jsondata eines files zu bekommen
returns: None if file is empty
			dictionary else
"""
def get_data_from_file(path):
	if not(os.stat(path).st_size == 0):
		f = open(path, "r")
		data= json.load(f)
		f.close()
		return data
	else:
		return None


#dump data to in jsonformat to jsonfile
def dump_data_to_file(data, path):
	f = open(path, "w+")
	json.dump(data, f, indent=4)
	f.close()


def is_json(file):
    try:
        json_object = json.load(file)
    except ValueError:
        print('invalid json')
        return False
    return True


