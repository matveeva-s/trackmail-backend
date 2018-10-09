def application (env, start_resp):
	start_resp('200 OK', [ ('Content-Type': 'text/plain') ])
	return ['Hello there!' ]	
