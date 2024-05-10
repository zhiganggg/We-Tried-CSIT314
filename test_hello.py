import unittest, time
from flask import Flask
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
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

    def test_login_page_post_success(self):
        response = self.app.post('/login', data=dict(email='test@example.com', password='test_password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Print the redirected URL if there is one
        time.sleep(10)
        print("Redirected to:", response.location)
        # self.assertIn(b'Logged in successfully', response.data)
        
    
    def test_buy_page_requires_login(self):
        response = self.app.get('/buy')
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        print("[Buy]Redirected to:", response.location)

    

if __name__ == '__main__':
    unittest.main()
