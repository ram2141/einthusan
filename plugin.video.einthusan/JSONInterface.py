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

get_movie_detail(20)
##
#
##
def get_list():
	login_url = 'http://www.einthusan.com/webservice/filters.php'
	form_data = {}
	form_data['lang'] = 'tamil'
	form_data['organize'] = 'Rating'
	form_data['filtered'] = 'Comedy'

	result = HTTPInterface.http_post(login_url, form_data)

	a = json.loads(result)
	test = a['results']

	print get_video_detail(50)

	#for sad in test:
		#print sad
