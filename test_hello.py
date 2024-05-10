import unittest, time
from flask import Flask
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
from run import app
from app.entity.entity import User  # Assuming your User model is in models.py
from werkzeug.security import generate_password_hash, check_password_hash

class FlaskTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            # Create a user for testing
            user = User.create_user(email='test@example.com', first_name='Test', last_name='User', password=generate_password_hash('test_password', method="pbkdf2:sha256"), profile_id=2)

    def test_login_page_post_success(self):
        print('\n=====test_login_page_post_success=====')
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

    def test_login_page_post_unsuccess(self):
        print('\n=====test_login_page_post_unsuccess=====')
        # Scenario 1: Incorrect Password
        response = self.app.post('/login', data=dict(email='test@example.com', password='test_password123'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        if response.status_code == 200:
            if "Logged in successfully!" in response.text:
                print("Login successful")
            elif "Incorrect password, try again." in response.text:
                print("Scenario 1 Error: Incorrect password, try again.")
            elif "Your account is disabled. Please contact support." in response.text:
                print("Scenario 2 Error: Your account is disabled. Please contact support.")
            elif "User does not exist." in response.text:
                print("Scenario 3 Error: User does not exist.")
            else:
                print("Error login")

        # Scenario 2: disabled account
        response = self.app.post('/login', data=dict(email='test@example.com', password='test_password123'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        if response.status_code == 200:
            if "Logged in successfully!" in response.text:
                print("Login successful")
            elif "Incorrect password, try again." in response.text:
                print("Scenario 1 Error: Incorrect password, try again.")
            elif "Your account is disabled. Please contact support." in response.text:
                print("Scenario 2 Error: Your account is disabled. Please contact support.")
            elif "User does not exist." in response.text:
                print("Scenario 3 Error: User does not exist.")
            else:
                print("Error login")

        # Scenario 3: User did not exist
        response = self.app.post('/login', data=dict(email='testnoexist@example.com', password='test_password123'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        if response.status_code == 200:
            if "Logged in successfully!" in response.text:
                print("Login successful")
            elif "Incorrect password, try again." in response.text:
                print("Scenario 1 Error: Incorrect password, try again.")
            elif "Your account is disabled. Please contact support." in response.text:
                print("Scenario 2 Error: Your account is disabled. Please contact support.")
            elif "User does not exist." in response.text:
                print("Scenario 3 Error: User does not exist.")
            else:
                print("Error login")

    def test_signup_page_post_success(self):
        print('\n=====test_signup_page_post_success=====')
        response = self.app.post('/sign-up', data=dict(email='test@example.com', first_name='Test', last_name='User',
                                                          password='test_password', verify_password='test_password',
                                                          profile=2, cea_registration_no='', agency_license_no=''), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        if response.status_code == 200:
            if "Account created!" in response.text:
                print("Account created!")
            elif "User already exists" in response.text:
                print("User already exists")
        print('test_signup_page_post_success redirect:', response.location)
        
    def test_buy_page_requires_login(self):
        response = self.app.get('/buy')
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        print("[Buy]Redirected to:", response.location)

if __name__ == '__main__':
    unittest.main()
