#Con la creacion de este archivo convertimos este directorio como un paquete.
# auth será el blueprint tanto el registro como cel login del usuario

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bootstrap = Bootstrap()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "authentication.log_in_user"
login_manager.session_protection = "strong"

def create_app(config_type):
    app = Flask( __name__ )
    configuration = os.path.join(os.getcwd(), "config", config_type + ".py") # eso se ubica sobre la careta config 
    app.config.from_pyfile(configuration)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.auth import authentication
    app.register_blueprint(authentication)

    return app

