import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy 

from app import create_app
from models import setup_db, Movie, Actor

ca_cred = os.environ['CA_CRED']
cd_cred = os.environ['CD_CRED']
ep_cred = os.environ['EP_CRED']


class CastingTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app()
		self.client = self.app.test_client
		#self.database_name = "casting"
		#self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', self.database_name)
		self.database_path = os.environ['DATABASE_URL']
		setup_db(self.app, self.database_path)

		with self.app.app_context():
			self.db = SQLAlchemy()
			self.db.init_app(self.app)
			self.db.create_all()

	def tearDown(self):
		pass

	#POST
	def test_pass_create_actor(self):
		res = self.client().post('/actors', json={"name": "David", "age": "22", "gender": "male"}, headers={"Authorization": f"Bearer {cd_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['actor'])

	def test_fail_create_actor(self):
		res = self.client().post('/actors', json={"age": "22", "gender": "male"}, headers={"Authorization": f"Bearer {cd_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 422)
		self.assertEqual(data['success'], False)

	def test_pass_create_movie(self):
		res = self.client().post('/movies', json={"title": "winners", "release_date": "02-02-2020"}, headers={"Authorization": f"Bearer {ep_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['movie'])

	def test_fail_create_movie(self):
		res = self.client().post('/movies', json={"release_date": "02-02-2020"}, headers={"Authorization": f"Bearer {ep_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 422)
		self.assertEqual(data['success'], False)


	#GET
	def test_pass_get_actors(self):
		res = self.client().get('/actors', headers={"Authorization": f"Bearer {ca_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['actors'])

	def test_fail_get_actors(self):
		res = self.client().delete('/actors', headers={"Authorization": f"Bearer {ca_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 405)
		self.assertEqual(data['success'], False)

	def test_pass_get_actor(self):
		res = self.client().get('/actors/8', headers={"Authorization": f"Bearer {ca_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['actor'])

	def test_fail_get_actor(self):
		res = self.client().get('/actors/1000', headers={"Authorization": f"Bearer {ca_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 422)
		self.assertEqual(data['success'], False)

	def test_pass_get_movies(self):
		res = self.client().get('/movies', headers={"Authorization": f"Bearer {ca_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['movies'])

	def test_fail_get_movies(self):
		res = self.client().delete('/movies', headers={"Authorization": f"Bearer {ca_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 405)
		self.assertEqual(data['success'], False)

	def test_pass_get_movie(self):
		res = self.client().get('/movies/9', headers={"Authorization": f"Bearer {ca_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['movie'])

	def test_fail_get_movie(self):
		res = self.client().get('/movies/1000', headers={"Authorization": f"Bearer {ca_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 422)
		self.assertEqual(data['success'], False)

	#PATCH
	def test_pass_patch_actor(self):
		res = self.client().patch('/actors/8', json={"gender": "female"}, headers={"Authorization": f"Bearer {cd_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['actor'])
		

	def test_fail_patch_actor(self):
		res = self.client().patch('/actors/1000', json={"gender": "female"}, headers={"Authorization": f"Bearer {cd_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 422)
		self.assertEqual(data['success'], False)

	def test_pass_patch_movie(self):
		res = self.client().patch('/movies/9', json={"release_date": "02-02-2022"}, headers={"Authorization": f"Bearer {ep_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['movie'])
		

	def test_fail_patch_movie(self):
		res = self.client().patch('/movies/1000', json={"release_date": "02-02-2022"}, headers={"Authorization": f"Bearer {ep_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 422)
		self.assertEqual(data['success'], False)

	#GET
	def test_pass_get_actors(self):
		res = self.client().get('/actors', headers={"Authorization": f"Bearer {ca_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['actors'])

	def test_pass_get_movies(self):
		res = self.client().get('/movies', headers={"Authorization": f"Bearer {ca_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['movies'])

	#DELETE
	def test_pass_delete_actor(self):
		res = self.client().delete('/actors/7', headers={"Authorization": f"Bearer {ep_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['actor'])

	def test_fail_delete_actor(self):
		res = self.client().delete('/actors/1000', headers={"Authorization": f"Bearer {cd_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 422)
		self.assertEqual(data['success'], False)

	def test_pass_delete_movie(self):
		res = self.client().delete('/movies/8', headers={"Authorization": f"Bearer {ep_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['movie'])

	def test_fail_delete_movie(self):
		res = self.client().delete('/movies/1000', headers={"Authorization": f"Bearer {ep_cred}"})
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 422)
		self.assertEqual(data['success'], False)

if __name__ == "__main__":
	unittest.main()