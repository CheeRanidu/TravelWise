import unittest
from unittest.mock import patch, Mock
from app import app  
from flask import json


class SignupTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('user.collection.find_one')
    @patch('user.request')
    def test_missing_required_fields(self, mock_request, mock_find_one):
        mock_request.get_json.return_value = {
            'email': 'john@example.com',
            'password': 'password123',
            
        }
        response = self.app.post('/signup', data=json.dumps(mock_request.get_json()), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Email, name, and password are required')

    @patch('user.collection.find_one')
    @patch('user.request')
    def test_email_already_exists(self, mock_request, mock_find_one):
        mock_request.get_json.return_value = {
            'email': 'john@example.com',
            'firstName': 'John',
            'password': 'password123',
        }
        mock_find_one.return_value = {'email': 'john@example.com'}  
        response = self.app.post('/signup', data=json.dumps(mock_request.get_json()), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Email already registered')

    @patch('user.collection.insert_one')
    @patch('user.collection.find_one')
    @patch('user.request')
    def test_successful_signup(self, mock_request, mock_find_one, mock_insert_one):
        mock_request.get_json.return_value = {
            'email': 'john@example.com',
            'firstName': 'John',
            'password': 'password123',
        }
        mock_find_one.return_value = None  
        response = self.app.post('/signup', data=json.dumps(mock_request.get_json()), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'Registration successful')

if __name__ == '__main__':
    unittest.main()


        

if __name__ == '__main__':
    unittest.main()
