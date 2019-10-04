import re
import json
import traceback

class Register:
	"""
	Singleton class that acts as a store of all the potential resources and associated calls available in a given API. 
	"""

	_registry = {}

	def __new__(self):
		if not hasattr(self, 'instance'):
		  self.instance = super().__new__(self)
		return self.instance

	def __len__(self):
		"""
		Returns the total count of method calls that have been registered
		"""
		return len(Register._registry)

	def _register(self, key, class_, fn):
		"""
		Function adds a record to the _registry dictionary attributed attached to the Resources singleton instance
		"""
		self._registry[key] = (class_, fn)

	def _methods(self, route):
		"""
		Function takes a given route and pulls all unbound functions. These functions will be unbound because the class will be uninstantiated when the method is run. 

		Parameters
		----------
		route : <Class>
			class object that is associated with an API route or "path" these routes are also known as resources 
		
		Returns
		-------
		list
			Function returns an array of user defined methods associated with the given route. These will be inspected against a given event dictionary from the lambda proxy to determine the correct function to run. 

		"""
		return [f for f in i.getmembers(route) if i.isfunction(f[1])]

	def add(self, verb = "POST", route = None):
		"""	"""

		class class_decorator:
			
			def __init__(self, fn):
				self.fn = fn

			def __set_name__(self, owner, name):
				# do something with owner, i.e.
				# print(key)
				# key = self.rk or owner.__name__.lower() + "/"
				key = route or owner.__name__.lower() + "/"
				Register._registry[key] = {verb : {"class_": owner, "func": self.fn}}

				# then replace ourself with the original method
				setattr(owner, name, self.fn)

		return class_decorator

	def get(self, key):

		return Register._registry.get(key, None)

	def __getitem__(self, key):

		return Register._registry[key]



r = Register()
class Something:

	@r.add(verb = "GET", route = "blah")
	def somefunc(self):
		return "bar"


print(r._registry)

class Handler:

	def __init__(self, event, context = None, **kw):
		"""
		Call constructure captures inputs from lambda proxy call
		"""
		self.params = {}
		self.event = event  
		self.context = context
		self.status = 200
		self.registry = Register()
		self._parse_event() # set call components
		 

	def _parse_event(self):

		self._update_params()
		self._set_class_func()

	def _update_params(self):
		"""
		Function updates the params dictionary with all passed variables 
		"""
		q =  self.event.get("queryStringParameters", {})
		m = self.event.get("multiValueQueryStringParameters", {})
		self.params.update(q)
		self.params.update(m)

	def _set_class_func(self):
		"""
		fuction searches the registry and gets associated class and function
		"""
		resource = self.registry.get(self.event["path"])
		data = resource.get(self.event["httpMethod"], None)
		self.class_ = data["class_"]
		self.func = data["func"]

	def _set_response(self):
		self.response =  {"isBase64Encoded": False,
					"statusCode": self.status,
					"headers":{
				"X-Requested-With": "*",
				"Access-Control-Allow-Origin": "*",
				"Access-Control-Allow-Methods": "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
				"Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
			}}


	def run(self, *args, **kw):
		body = {}
		try:
			c = self.class_(*args, **kw)
			body = json.dumps(self.func(c, **self.params))
			self.response["body"] = body
		except Exception:
			self.status = 400
			exc_type, exc_value, exc_traceback = (
				sys.exc_info()
			)  # get stack trace for error
			body = traceback.format_exception(
				exc_type, exc_value, exc_traceback
			)  # dumping stack
			raise
		finally:
			self._set_response()
			return self.response

		



# {
#             "isBase64Encoded": False,
#             "statusCode": status_code,
#             "headers": {
#                 "X-Requested-With": "*",
#                 "Access-Control-Allow-Origin": "*",
#                 "Access-Control-Allow-Methods": "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
#                 "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
#             },
#             "body": json.dumps(body),
#         }

test = {
   "resource":"/{proxy+}",
   "path":"users/123/requests/1/",
   "httpMethod":"GET",
   "headers":"Null",
   "multiValueHeaders":"Null",
   "queryStringParameters":{
	"nonsense":"blah"
	  # "notstuff":"users"123/requests/1
   },
   "multiValueQueryStringParameters":{
	  "stuff":[
		 "foo",
		 "bar"
	  ]
   },
   "pathParameters":{
	  "proxy":"something/123/users"
   },
   "stageVariables":"Null",
   "requestContext":{
	  "resourceId":"tlpx5g",
	  "resourcePath":"/{proxy+}",
	  "httpMethod":"GET",
	  "extendedRequestId":"AvfiBE7QvHcFq1g=",
	  "requestTime":"28/Sep/2019:18:54:43 +0000",
	  "path":"/{proxy+}",
	  "accountId":"911808035826",
	  "protocol":"HTTP/1.1",
	  "stage":"test-invoke-stage",
	  "domainPrefix":"testPrefix",
	  "requestTimeEpoch":1569696883211,
	  "requestId":"98f2ea03-1b91-4b9b-a69f-13ccdfe597bb",
	  "identity":{
		 "cognitoIdentityPoolId":"Null",
		 "cognitoIdentityId":"Null",
		 "apiKey":"test-invoke-api-key",
		 "principalOrgId":"Null",
		 "cognitoAuthenticationType":"Null",
		 "userArn":"arn:aws:iam::911808035826:root",
		 "apiKeyId":"test-invoke-api-key-id",
		 "userAgent":"aws-internal/3 aws-sdk-java/1.11.633 Linux/4.9.184-0.1.ac.235.83.329.metal1.x86_64 OpenJDK_64-Bit_Server_VM/25.222-b10 java/1.8.0_222 vendor/Oracle_Corporation",
		 "accountId":"911808035826",
		 "caller":"911808035826",
		 "sourceIp":"test-invoke-source-ip",
		 "accessKey":"ASIA5IS76PPZJGDW7P6C",
		 "cognitoAuthenticationProvider":"Null",
		 "user":"911808035826"
	  },
	  "domainName":"testPrefix.testDomainName",
	  "apiId":"hnr5hcfad3"
   },
   "body":"Null",
   "isBase64Encoded":False
}

r = Register()
print(r._registry)



# c = Call(test)
# print(c.params)
# print(c.class_)
# print(c.func)
# print(c.run())