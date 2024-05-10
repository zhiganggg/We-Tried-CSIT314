import unittest
from flask import Flask
from run import app

class FlaskTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        
    def test_buy_page_requires_login(self):
        response = self.app.get('/buy')
        self.assertEqual(response.status_code, 302)  # Redirect to login page

if __name__ == '__main__':
    unittest.main()
