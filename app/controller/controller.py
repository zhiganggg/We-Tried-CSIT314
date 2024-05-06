from app.entity.entity import *
from flask import flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

class loginController:
    def retrieveUser(self, email):
        return User.get_user_by_email(email)