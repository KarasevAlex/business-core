from flask import Flask, Blueprint, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import flask_excel as excel
from flask_mail import Mail
from flask_login import AnonymousUserMixin


class Anonymous(AnonymousUserMixin):
   def isAdmin(self):
       return False

def err_404(e):
    return redirect('/404')
def err_401(e):
    return redirect('/401')
def err_500(e):
    return redirect('/500')

from config import config


main = Blueprint('main', __name__)
db = SQLAlchemy()
loginManager = LoginManager()
loginManager.session_protection = "basic"
loginManager.anonymous_user = Anonymous
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    db.init_app(app)
    loginManager.init_app(app)
    excel.init_excel(app)
    from .main import main as main_bp
    app.register_blueprint(main_bp)
    mail.init_app(app)
    app.register_error_handler(404, err_404)
    app.register_error_handler(401, err_401)
    app.register_error_handler(500, err_500)

    return app