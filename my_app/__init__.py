#__int__ is intialization it runs automatically whenever we call my_app
# thus conforming that all the pre-requites are met

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Resource , Api
import datetime
app = Flask(__name__)
api=None
api=Api(app)   #api settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///track_it_all.db'
app.config['SECRET_KEY']='adb17a378fb857c96f99b63f26c7b1'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="login_page"
login_manager.login_message_category="info"

from my_app import routes
