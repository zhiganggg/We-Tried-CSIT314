from flask import Flask

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = '1H{LkD*3oWf$8yU!q2RzN@7vP'

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  return app
  