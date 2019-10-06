


someset = set()

someset.add("users")
someset.add("requests")

print(someset)


stuff = "/users/123/requests/1/"
event = {"path": stuff}

class Handler:

	def __init__(self, event, context = None, *args, **kw):

		self.route_list = []
		self.arg_list = []
		self.event = event
		self.context = context
		self._handle_path()


	def add_stuff(self, something):
		if something:
			if something in someset:
				self.route_list.append(something)
			else:
				print("this happened")
				self.arg_list.append(something)

	def _handle_path(self):
		path = self.event.get("path", None)
		if path:
			[self.add_stuff(i) for i in path.split("/")]


h = Handler(event)
print(h.route_list)
print(h.arg_list)

