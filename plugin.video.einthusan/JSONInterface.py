import json

import HTTPInterface

##
# Gets the details when a movie id is passed.
#
# Returns a tuple as follows:
# 			(id, name, picture_url)
##

def get_movie_detail(movie_id):
	API_URL = 'http://www.einthusan.com/webservice/movie.php?id=' + str(movie_id)
	html = HTTPInterface.http_get(API_URL)
	response_json = json.loads(html)
	return response_json['movie_id'], response_json['movie'], response_json['cover']
##
# Returns a list of movie id for a specific filters
# returns json decoded of the response from the server
##
def apply_filter(filters):
	API_URL = 'http://www.einthusan.com/webservice/filters.php'

	result = HTTPInterface.http_post(API_URL, data=filters)
	return  json.loads(result)