import time
from util import *


#AI class that returns the intent of the request and the keywords
class Wit:
	def __init__(self, *request, **keywordrequest):

		data = get_data_from_file('intent.json')
		self.intent_keywords = set()

		for k in data:
			self.intent_keywords.update(data[k])
			print(self.intent_keywords)

		data = get_data_from_file('capitals.json')
		self.location_set = set()

		if 'capitals' in data:
			location_params = data['capitals']
			self.location_set = set(location_params)
		else:
			print("Somewthing went wrong with captials.json")

		data = get_data_from_file('german_cities.json')
		if 'Germany' in data:
			location_params = data['Germany']
			data = None
			self.location_set.update(location_params)
			location_params = None
			#print(self.location_set)
		else:
			print("Seomthing went wrong with german_cities.json")
		

	def getIntent(request):
		if request in self.intent_keywords:
			pass
		pass

	def analyze_request(self, request):
		start_time = time.time()
		if request in self.location_set:
			print(request + " is in the set.")
		else:
			print(request + " is not in the set.")
		print("--- %s seconds ---" % (time.time() - start_time))


	def learn_phrase(phrase):
		pass