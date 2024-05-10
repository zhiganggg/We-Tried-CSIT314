import unittest, time
from flask import Flask
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
from run import app
from app.entity.entity import User  # Assuming your User model is in models.py

class FlaskTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            # Create a user for testing
            user = User.create_user(email='test@example.com', first_name='Test', last_name='User', password='test_password', profile_id=2)

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_page_post_success(self):
        response = self.app.post('/login', data=dict(email='test@example.com', password='test_password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        if response.status_code == 200:
            if "Logged in successfully!" in response.text:
                print("Login successful")
            elif "Incorrect password, try again." in response.text:
                print("Error: Incorrect password, try again.")
            elif "Your account is disabled. Please contact support." in response.text:
                print("Error: Your account is disabled. Please contact support.")
            elif "User does not exist." in response.text:
                print("Error: User does not exist.")
            else:
                print("Error login")

    def test_signup_page_post_success(self):
        response = self.app.post('/sign-up', data=dict(email='test@example.com', first_name='Test', last_name='User',
                                                          password='test_password', verify_password='test_password',
                                                          profile='2', cea_registration_no='', agency_license_no=''), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_buy_page_requires_login(self):
        response = self.app.get('/buy')
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        print("[Buy]Redirected to:", response.location)

if __name__ == '__main__':
    unittest.main()
