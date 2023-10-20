import unittest
from unittest.mock import patch, Mock
from app import app  
from flask import json

class PartnerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('user.collection1.find_one')
    @patch('user.request')
    def test_national_id_already_exists(self, mock_request, mock_find_one):
     mock_request.get_json.return_value = {
        'name': 'John',
        'age': 30,
        'marital': 'Single',
        'interest': 'Hiking',
        'aboutme': 'I love nature',
        'nationalid': '1234567890',
        'email': 'john@example.com'
    }
     mock_find_one.return_value = {'nationalid': '1234567890'}
    
     with app.test_request_context():
           response = self.app.post('/partner', data=json.dumps(mock_request.get_json()), content_type='application/json')
           data = json.loads(response.data)
           self.assertEqual(response.status_code, 400)
           self.assertEqual(data['error'], 'user already registered')

    @patch('user.collection1.insert_one')
    @patch('user.collection1.find_one')
    @patch('user.request')
    def test_successful_registration(self, mock_request, mock_find_one, mock_insert_one):
        mock_request.get_json.return_value = {
            'name': 'John',
            'age': 30,
            'marital': 'Single',
            'interest': 'Hiking',
            'aboutme': 'I love nature',
            'nationalid': '1234567890',
            'email': 'john@example.com'
        }
        mock_find_one.return_value = None  
        response = self.app.post('/partner', data=json.dumps(mock_request.get_json()), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'Registration successful')

if __name__ == '__main__':
    unittest.main()
