# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
   app = Flask(__name__, template_folder="boundary")
   app.config["SECRET_KEY"] = "1H{LkD*3oWf$8yU!q2RzN@7vP"
   app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
   db.init_app(app)

   # Import and register blueprints
   from .controller.controller import controller
   app.register_blueprint(controller)

   from .entity.entity import User

   with app.app_context():
      db.create_all()

   login_manager = LoginManager()
   login_manager.login_view = "controller.login"
   login_manager.init_app(app)

   @login_manager.user_loader
   def load_user(id):
      return User.query.get(int(id))

   return app

def create_database(app):
   if not path.exists("app/" + DB_NAME):
      db.create_all(app=app)
      print('Created Database!')