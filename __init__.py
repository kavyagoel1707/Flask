from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
import pymysql
db = SQLAlchemy()

def create_app():
    app = Flask(__name__) #creates the Flask instance
    app.config['SECRET_KEY'] = 'secret-key-goes-here'#to keep data safe  
    username='root'
    password='root'
    dbname='/kavya'
    userpass='mysql+pymysql://' + username + ':' + password + '@'
    server='127.0.0.1'
    app.config['SQLALCHEMY_DATABASE_URI'] = userpass+server+dbname #path where sqlite database will be saved

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #deactivate Flask-SQLAlchemy sqlite database
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    db.init_app(app) #initialize sqlite database
    login_manager = LoginManager() #creating login manager instance
    login_manager.login_view='auth.login' #defining redirection
    login_manager.init_app(app) #configuring
    from models import User
    @login_manager.user_loader
    #reloading user objects
    def load_user(user_id):
        return User.query.get(int(user_id))
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from upload import upload as upload_blueprint
    app.register_blueprint(upload_blueprint)
    return app