# run.py is responsible for executing files 
# save this as app.py
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db' # 🔗 DATABASE CONNECTED HERE
app.config['SECRET_KEY']='cba2ebf3374e4dbb712a44be' # secret key for forms
db=SQLAlchemy(app)# yhha modules.py me shift karne e baad  app me error aaya baki sab import karke coz app file ko iss file me import karmna forbidden hai uske liye apan ne run.py banayi
 
bcrypt= Bcrypt(app) # for hashing passwords

login_manager= LoginManager(app) # for user session management

login_manager.login_view="login_page" # this is the name of the login route, so that if user tries to access a page that requires login, they will be redirected to this page
login_manager.login_message_category='info' # this is the category of the flash message that will be shown when user is redirected to login page
from market.models import Item, User # Import your models here
from market import routes # to register your routes/views