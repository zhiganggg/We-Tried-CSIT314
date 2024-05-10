import unittest
from flask import Flask
from run import app

class FlaskTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_signup_page_post_success(self):
        response = self.app.post('/sign-up', data=dict(email='test@example.com', first_name='Test', last_name='User',
                                                          password='test_password', verify_password='test_password',
                                                          profile='2', cea_registration_no='', agency_license_no=''), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_buy_page_requires_login(self):
        response = self.app.get('/buy')
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    

if __name__ == '__main__':
    unittest.main()
