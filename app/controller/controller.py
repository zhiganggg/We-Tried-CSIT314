from app.entity.entity import *
from flask import flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

class loginController:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def loginUser(self):
        user = User.get_user_email(self.email)
        if user:
            if user.status.value == "ENABLED":
                if check_password_hash(user.password, self.password):
                    # Login success
                    login_user(user, remember=True)
                    return 'success', 'Logged in successfully!'
                else:
                    return 'error', 'Incorrect password, try again.'     
            else:
                return 'error', 'Your account is disabled. Please contact support.'
        else:
            return 'error', 'Email does not exist.'