import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from authentication import AuthError, requires_auth
from models import Movie, Actor, setup_db
import sys

def create_app(test_config=None):
  # create and configure the app
	app = Flask(__name__)
	setup_db(app)
	CORS(app)


	#gets all actors in the db
	#returns json containing an array of the actors
	@app.route('/actors')
	@requires_auth('get:actors')
	def get_actors(payload):
		actors_obj = []
		actors_formatted = []

		try:
			actors_obj = Actor.query.all()
			actors_formatted = [actor.format() for actor in actors_obj]
			return jsonify({
				"success": True,
				"actors": actors_formatted
				})
		except:
			abort(422)

	#gets all movies in the db
	#returns json containing an array of the movies
	@app.route('/movies')
	@requires_auth('get:movies')
	def get_movies(payload):
		movies_obj = []
		movies_formatted = []

		try:
			movies_obj = Movie.query.all()
			movies_formatted = [movie.format() for movie in movies_obj]
			return jsonify({
				"success": True,
				"movies": movies_formatted
				})
		except:
			abort(422)

	#gets an actor with a specific id
	#returns json containing a dict representation of the actor
	@app.route('/actors/<int:actor_id>')
	@requires_auth('get:actors')
	def get_actor(payload, actor_id):
		try:
			actor_obj = Actor.query.filter_by(id=actor_id).one_or_none()
			if actor_obj is None:
				abort(422)
			return jsonify({
				"success": True,
				"actor": actor_obj.format()
				})
		except:
			abort(422)

	#gets a movie with a specific id
	#returns json contanining a dict representation of the movie
	@app.route('/movies/<int:movie_id>')
	@requires_auth('get:movies')
	def get_movie(payload, movie_id):
		try:
			movie_obj = Movie.query.filter_by(id=movie_id).one_or_none()
			if movie_obj is None:
				abort(422)
			return jsonify({
				"success": True,
				"movie": movie_obj.format()
				})
		except:
			abort(422)

	#creates an actor in the db if all fields are given
	#returns the created actor as a dict representation
	@app.route('/actors', methods=['POST'])
	@requires_auth('post:actor')
	def create_actor(payload):
		try:
			body = request.get_json()
			name = body.get('name', None)
			age = body.get('age', None)
			gender = body.get('gender', None)
			if name is None:
				abort(422)
			if age is None:
				abort(422)
			if gender is None:
				abort(422)
			actor = Actor(name=name, age=age, gender=gender)
			actor.insert()

			return jsonify({
				"success": True,
				"actor": actor.format()
			})
		except:
			abort(422)

	#modifies an actor in the db
	#returns the modified actor as a dict represention
	@app.route('/actors/<int:actor_id>', methods=['PATCH'])
	@requires_auth('patch:actor')
	def modify_actor(payload, actor_id):
		try:
			actor = Actor.query.filter_by(id=actor_id).one_or_none()
			if actor is None:
				abort(422)
			body = request.get_json()
			name = body.get('name', None)
			age = body.get('age', None)
			gender = body.get('gender', None)
			if name is not None:
				actor.name = name
			if age is not None:
				actor.age = age
			if gender is not None:
				actor.gender = gender

			actor_formatted = actor.format()
			
			actor.update()

			return jsonify({
				"success": True,
				"actor": actor_formatted
			})
		except:
			abort(422)

	#creates a movie in the db
	#returns the movie as a dict representation
	@app.route('/movies', methods=['POST'])
	@requires_auth('post:movie')
	def create_movie(payload):
		try:
			body = request.get_json()
			title = body.get('title', None)
			release_date = body.get('release_date', None)

			if title is None:
				abort(422)
			if release_date is None:
				abort(422)

			movie = Movie(title=title, release_date=release_date)
			movie.insert()

			return jsonify({
				"success": True,
				"movie": movie.format()
			})

		except:
			abort(422)

	#modifies a movie in the db
	#returns the movie as dict representation
	@app.route('/movies/<int:movie_id>', methods=['PATCH'])
	@requires_auth('patch: movie')
	def modify_movie(payload, movie_id):
		try:
			movie = Movie.query.filter_by(id=movie_id).one_or_none()
			if movie is None:
				abort(422)
			body = request.get_json()
			title = body.get('title', None)
			release_date = body.get('release_date', None)

			if title is not None:
				movie.title = title
			if release_date is not None:
				movie.release_date = release_date

			movie_formatted = movie.format()
			
			movie.update()

			return jsonify({
				"success": True,
				"movie": movie_formatted
			})

		except:
			abort(422)

	#deletes an actor from the db
	#returns the deleted actor in dict format
	@app.route('/actors/<int:actor_id>', methods=['DELETE'])
	@requires_auth('delete:actor')
	def delete_actor(payload, actor_id):
		try:
			actor = Actor.query.filter_by(id=actor_id).one_or_none()
			if actor is None:
				abort(422)
			actor_formatted = actor.format()
			actor.delete()

			return jsonify({
				"success": True,
				"actor": actor_formatted
			})
		except:
			abort(422)

	#deletes a movie from the db
	#returns the deleted movie in dict representation
	@app.route('/movies/<int:movie_id>', methods=['DELETE'])
	@requires_auth('delete:movie')
	def delete_movie(payload, movie_id):
		try:
			movie = Movie.query.filter_by(id=movie_id).one_or_none()
			if movie is None:
				abort(422)
			movie_formatted = movie.format()
			movie.delete()

			return jsonify({
				"success": True,
				"movie": movie_formatted
			})
		except:
			abort(422)




	@app.errorhandler(422)
	def unprocessable(error):
	    return jsonify({
	                    "success": False, 
	                    "error": 422,
	                    "message": "unprocessable"
	                    }), 422

	@app.errorhandler(404)
	def not_found(error):
	    return jsonify({
	                    "success": False, 
	                    "error": 404,
	                    "message": "resource not found"
	                    }), 404

	@app.errorhandler(405)
	def method_not_allowed(error):
	    return jsonify({
	                    "success": False, 
	                    "error": 405,
	                    "message": "method not allowed"
	                    }), 405

	@app.errorhandler(500)
	def server_error(error):
	    return jsonify({
	                    "success": False, 
	                    "error": 500,
	                    "message": "server error"
	                    }), 500

	@app.errorhandler(AuthError)
	def auth_error(error):
		return jsonify({
			"success": False,
			"error": error.status_code,
			"message": error.error,
		}), error.status_code


	return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)