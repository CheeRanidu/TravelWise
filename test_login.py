import unittest
from unittest.mock import patch, Mock
from app import app  # Replace with your actual Flask app import
from flask import json
import pandas as pd

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('config.collection')  
    @patch('user.bcrypt')  
    def test_login_missing_fields(self, mock_bcrypt, mock_collection):
        response = self.app.post('/login', data=json.dumps({}), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Username and password are required')

#     @patch('config.collection')
#     def test_login_invalid_email(self, mock_collection):
#         mock_collection.find_one.return_value = None
#         response = self.app.post('/login', data=json.dumps({'email': 'invalid@example.com', 'password': 'password'}), content_type='application/json')
#         data = json.loads(response.data)
#         self.assertEqual(response.status_code, 401)
#         self.assertEqual(data['error'], 'Invalid credentials')

    @patch('config.collection')
    @patch('user.bcrypt')
    def test_login_invalid_password(self, mock_bcrypt, mock_collection):
        user_data = {'email': 'john@john.com', 'password': 'hashed_password'}
        mock_collection.find_one.return_value = user_data
        mock_bcrypt.checkpw.return_value = False
        response = self.app.post('/login', data=json.dumps({'email': 'john@john.com', 'password': '123'}), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['error'], 'Invalid credentials')

#     @patch('config.collection')
#     @patch('user.bcrypt')
#     @patch('app.jwt')
#     @patch('user.jwt.encode', return_value='valid_token')
#     def test_login_successful(self, mock_jwt, mock_bcrypt, mock_collection):
#         user_data = {'_id': 'some_id', 'email': 'john@john.com', 'password': 'joh123'}
#         mock_collection.find_one.return_value = user_data
#         mock_bcrypt.checkpw.return_value = True
#         mock_jwt.encode.return_value = 'valid_token'
#         response = self.app.post('/login', data=json.dumps({'email': 'john@john.com', 'password': 'joh123'}), content_type='application/json')
#         data = json.loads(response.data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(data['message'], 'Login successful')
#         self.assertIn('jwtToken=valid_token', response.headers['Set-Cookie'])

# class PredictTestCase(unittest.TestCase):

#     @patch('user.collection1.find')
#     # @patch('user.request')
#     def test_some_matching_profiles(self, mock_find):
#     # Mocking database to return some profiles, including one that should match
#      mock_find.return_value = [
#         {"aboutme": "I love hiking and adventures", "age": 26, "interest": "Mountains", "marital": "Single", "name": "Charlie", "email": "charlie@example.com"},
#         {"aboutme": "I love reading", "age": 30, "interest": "Books", "marital": "Married", "name": "Alice", "email": "alice@example.com"},
#     ]
    
#      with app.test_request_context():
#         with patch('user.request.get_json', return_value={
#             'age': 25,
#             'ms': 'Single',
#             'trvl': 'Hiking',
#             'myself': 'I love adventures'
#         }):
#             response = self.app.post('/predict', content_type='application/json')
#             data = json.loads(response.data)
#             self.assertEqual(response.status_code, 201)
#             self.assertGreater(len(data['profiles']), 0)  # At least one profile should match
#             self.assertIn("Charlie", [profile["name"] for profile in data['profiles']])  # Charlie should be in the recommended profiles

        

if __name__ == '__main__':
    unittest.main()
