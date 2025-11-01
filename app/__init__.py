#where I create the create_app function
from flask import Flask
from .models import db
from .extensions import ma
from .blueprints.runners import runners_bp
from .blueprints.teams import teams_bp
from flask_cors import CORS

#create the application factory
def create_app(config_name):
        
    #initialze blank app
    app = Flask(__name__)
    #configure the app
    app.config.from_object(f'config.{config_name}')
    CORS(app)

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(runners_bp,url_prefix='/runners')
    app.register_blueprint(teams_bp,url_prefix='/teams')

    return app