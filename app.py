from flask import Flask, jsonify, request
import csv, sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE movies (release_year TEXT, title TEXT, origin TEXT, director TEXT, cast TEXT, genre TEXT, wiki_page TEXT, plot TEXT);")

with open('movies.csv','r') as movie_table: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(movie_table) # comma is default delimiter
    to_db = [(i['release_year'], i['title'], i['origin'], i['director'], i['cast'], i['genre'], i['wiki_page'], i['plot']) for i in dr]


cursor.executemany("INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?, ?, ?)", to_db)
conn.commit()
conn.close()


@app.route("/")
def hello_world():
  return "Hello world"

'''
Name: /index
Inputs: None
Description: Index endpoint is called when retrieving all movies. 
'''
@app.route("/index", methods=["GET"])
def index():
  conn = sqlite3.connect("movies.db")
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM movies LIMIT 10")
  movies = cursor.fetchall()
  return jsonify(movies=movies)

@app.route("/search", methods=["POST"])
def search():
  pass

'''
Name: /add
Inputs: movie object 
Description: Add endpoint is called when using movie form to add another movie to the database. 
'''
@app.route("/add", methods=["POST"])
def add():
  data = request.json
  conn = sqlite3.connect("movies.db")
  cursor = conn.cursor()
  movie = {"release_year": data["movieObj"]["release_year"], "title": data["movieObj"]["title"],"origin": data["movieObj"]["origin"], "director": data["movieObj"]["director"], "cast": data["movieObj"]["cast"], "genre": data["movieObj"]["genre"], "wiki_page": data["movieObj"]["wiki_page"], "plot": data["movieObj"]["plot"]}
  cursor.execute("INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?, ?, ?)", movie)
  cursor.execute("SELECT * FROM movies LIMIT 10")
  movies = cursor.fetchall()
  return jsonify(movies=movies)

'''
Name: /edit
Inputs: movie object 
Description: Edit endpoint is called when using movie form to edit a movie to the database. 
'''
@app.route("/edit", methods=["PUT"])
def edit():
  pass


'''
Name: /delete
Inputs: movie object 
Description: Delete endpoint is called when deleting a movie from the database. 
'''
@app.route("/delete", methods=["DELETE"])
def delete():
  pass


if __name__ == "__main__":
  app.run()