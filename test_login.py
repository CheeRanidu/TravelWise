import unittest
from unittest.mock import patch, Mock
from app import app  
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

    @patch('config.collection')
    def test_login_invalid_email(self, mock_collection):
        mock_collection.find_one.return_value = None
        response = self.app.post('/login', data=json.dumps({'email': 'invalid@example.com', 'password': 'password'}), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['error'], 'Invalid credentials')

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

 

        

if __name__ == '__main__':
    unittest.main()
