from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_recaptcha import ReCaptcha


import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["MAIL_SERVER"] = "smtp.dreamhost.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv('MAIL_USER')
app.config["MAIL_PASSWORD"] = os.getenv('MAIL_PASS')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)


recaptcha = ReCaptcha()
recaptcha.is_enabled = True
recaptcha.site_key = os.getenv('RECAPTCHA_PUBLIC')
recaptcha.secret_key = os.getenv('RECAPTCHA_SECRET')
recaptcha.theme = 'light'
recaptcha.type = 'image'
recaptcha.size = 'normal'
recaptcha.tabindex = 0
recaptcha.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message_category = 'info'

from domdit import routes

