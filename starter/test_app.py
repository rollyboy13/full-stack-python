import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy 

from app import create_app
from models import setup_db, Movie, Actor

ca_cred = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdVcWc2Rnc2em5lWV9UZjVqTHJldiJ9.eyJpc3MiOiJodHRwczovL2ZzLXJvbGx5LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjEzMGY2YTY3ZjE5NDAwMTk5Y2M2MTgiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk1MTEwNzc3LCJleHAiOjE1OTUxMTc5NzcsImF6cCI6InZCTUQzWlczNkxwdWVUanA0V1o0eG10TndPQzdmNDdVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.ZBAJzSM5Ed3KMPEpR5B-f8nl8HaBmwADp1DogveChg_8P6l-kJoeuGIQqFgQtdWlGPeGmEvlotzevCClPQTWUGu_fngkdX_bp_GabP3qofxG57F4oRkDIOIGiV4jrr9VYus5PKAQaaZQtqjbc2ywQBY3IyeyDaFDLv5g98tAg136e6d2ZqrZo0KKhT3gxgjW1MweIC4tlQhZjR1V3IbKH3ujQzrBoccNkVi0masOHLgOD_Q2frNQ7BZbk0fXzQMTcwbC7ZZEmJsGBsM9hOLNY3UzMGK0dSoJIiaSkWn2zVT50bvvmmS63FYajR7si2uhIkhhIh8AMV8Qpp33q8g8nA"
cd_cred = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdVcWc2Rnc2em5lWV9UZjVqTHJldiJ9.eyJpc3MiOiJodHRwczovL2ZzLXJvbGx5LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjEzMTAwZjhhMGVkODAwMTMzMTcyMjUiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk1MTEwODQ2LCJleHAiOjE1OTUxMTgwNDYsImF6cCI6InZCTUQzWlczNkxwdWVUanA0V1o0eG10TndPQzdmNDdVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6IG1vdmllIiwicG9zdDphY3RvciJdfQ.B9jWu8t448XCtCL58CKgU48z7fuXfhEZZVgrqaCf6X417iVGG1wn1sw_2JvvEE3e0aYYTBw_zSnDSCMffpRUmIRw5OkBIk8D4IYM0OilF2iTdRs2aLOJP6i_KgGqEvbDNgZMDeII3RCZKtOmnhsO4EXMsDhSskzQKUUdc37uhg9VlY-xuKFbBWuYhOtiwc2aONX5pC9RIFJoEhuOWxkoJzMPYjRQyfgZRbuxNNc9j4p8GqT3VnWODpH5oqj4Yl9yBW-4YkBFpxxLpMGWFAPWke_dkUFUOrVNUht-rKrVhqc6TPTmXuW4Dnfm-hDC-J_C6seHttLqD5fZYXGzc4lhOA"
ep_cred = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdVcWc2Rnc2em5lWV9UZjVqTHJldiJ9.eyJpc3MiOiJodHRwczovL2ZzLXJvbGx5LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjEzMTA4YzhhMGVkODAwMTMzMTcyNWQiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk1MTEwOTEyLCJleHAiOjE1OTUxMTgxMTIsImF6cCI6InZCTUQzWlczNkxwdWVUanA0V1o0eG10TndPQzdmNDdVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6IG1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.jCzMZ7nws-r8zSoqMIHtb66nNfC-mKpDKDoiVhipKDqhzuyD_hGUwmFeNcHI86zNidOGM1oAh_37L2sJx0E_xmGPim0-gGV1LRJtr-6va8ksBuec8Hg4cCa_88EvT0cu96sR88fyzY9o_UnY41r8Eb2K09nMHtjVP70mgBXRM8EbzlAjLcSczf3-JcPnxQegZ51cEIaFrpt51_fUl_dgLuoIx0vwZz-pCh-YthmJBN8TVEnJJc8l_yTEDizppuJVWt-I2kRMoYSyiY1yn8URiKxGD27FetCn6GRqshJ9wnOjoIDAKwWIuQHP3SAPzmkBxdtAszGbe6O-N4QRiTGguw"



class CastingTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app()
		self.client = self.app.test_client
		self.database_name = "casting"
		self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', self.database_name)
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