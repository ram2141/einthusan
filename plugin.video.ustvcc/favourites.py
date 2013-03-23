import sqlite3

def initialise(db_path):

	conn = sqlite3.connect(db_path) # or use :memory: to put it in RAM
	 
	cursor = conn.cursor()
	 
	# create a table
	cursor.execute("""CREATE TABLE albums
	                  (title text, artist text, release_date text, 
	                   publisher text, media_type text) 
	               """)
class Tv_Show:
	string imdb_number


