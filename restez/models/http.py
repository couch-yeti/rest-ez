


class Response:

	def __init__(self, body, content_type = "application/json", cors= True, b64encode= False, **kw):
		self.cors = cors
		self.status = {
			"OK": 200,
			"EMPTY": 204,
			"NOK": 400,
			"FOUND": 302,
			"NOT_FOUND": 404,
			"CONFLICT": 409,
			"ERROR": 500,
		}
		self.binary_types - [
            "application/octet-stream",
            "application/x-protobuf",
            "application/x-tar",
            "application/zip",
            "image/png",
            "image/jpeg",
            "image/jpg",
            "image/tiff",
            "image/webp",
            "image/jp2",
        ]
	

	def _get_status(self, status):
		raise NotImplementedError


	def _set_response(self, body):

		