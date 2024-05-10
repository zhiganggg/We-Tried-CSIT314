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

    def test_buy_page_logged_in(self):
        # Login
        response = self.app.post('/login', data=dict(username='test_user', password='test_password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Logged in successfully' in response.data)

        # Access buy page after login
        response = self.app.get('/buy')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Buy Page', response.data)
        self.assertIn(b'Listings', response.data)  # Check if listings are rendered
        # Add more assertions as needed

if __name__ == '__main__':
    unittest.main()
