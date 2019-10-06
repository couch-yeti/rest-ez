import re

class Event(dict):

	"""
	What is it I want to achieve... 
	How do I want to interact with each of the components? 

	I need some sort of base function that takes the event from lambda
	and modifies it 
	"""
	def __init__(self, data):
		self.proxy = dict((self._key(k), k) for k in data)
		for k in self.proxy:
			self[k] = self.proxy[k]

	def _key(self, key):
		""" add underscore and lower case"""
		return re.sub("([A-Z]+)", r"_\1",key).lower()

	def __contains__(self, k):
		return k in self.proxy

	def __delitem__(self, k):
		key = self.proxy[k]
		super(Event, self).__delitem__(key)
		del self.proxy[k]

	def __getitem__(self, k):
		key = self.proxy[k]
		return super(Event, self).__getitem__(key)

	def get(self, k, default=None):
		return self[k] if k in self else default

	def __setitem__(self, k, v):
		super(Event, self).__setitem__(k, v)
		self.proxy[k] = k


class Headers(Event):

	def __init__(self, data):
		super().__init__(data)


class Context(Event):

	def __init__(self, data):
		if data.get("identity"):
			i = data.pop("identity")
			data["identity"] = Event(i)
			super().__init__(data)

	