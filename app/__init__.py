from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


from config import config



main = Blueprint('main', __name__)
db = SQLAlchemy()
loginManager = LoginManager()
loginManager.session_protection = "basic"

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    db.init_app(app)
    loginManager.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    return app