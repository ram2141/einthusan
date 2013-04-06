import sqlite3

##
# Looks at the cache and return the movie details.
##
def get_cached_movie_details(cache_db_file, id):
	conn = sqlite3.connect(cache_db_file)
	cursor = conn.cursor()

	# Check whether we have a table, otherwise create the table
	# Maybe there is a better way of doing this.
	cursor.execute('CREATE TABLE IF NOT EXISTS movie_detail_cache(id text, name text, image text)')
	cursor.execute('SELECT id, name, image FROM movie_detail_cache WHERE id=' + str(id))
	cached_results = cursor.fetchall()

	if (len (cached_results) > 0):
		return cached_results[0]


def save_move_details_to_cache(cache_db_file, id, name, picture):
	conn = sqlite3.connect(cache_db_file)
	cursor = conn.cursor()
	cursor.execute('INSERT INTO movie_detail_cache VALUES ("'+str(id)+'","'+str(name)+'","'+str(picture)+ '")')
	conn.commit()

movie_details = get_cached_movie_details("my_db.db", 12)
if (movie_details == None):
	save_move_details_to_cache("my_db.db", 12, 'Dus', 'dus_.jpg')
print get_cached_movie_details("my_db.db", 12)