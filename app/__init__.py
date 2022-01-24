from flask import Flask
from flask_mysql_connector import MySQL
from flask_bootstrap import Bootstrap
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, BOOTSTRAP_SERVE_LOCAL
from flask_wtf.csrf import CSRFProtect
import cloudinary
import cloudinary.uploader
import cloudinary.api


mysql = MySQL()
bootstrap = Bootstrap()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DATABASE=DB_NAME,
        MYSQL_HOST=DB_HOST,
        #BOOTSTRAP_SERVE_LOCAL=BOOTSTRAP_SERVE_LOCAL
    )
    cloudinary.config( 
        cloud_name = "dsemk8clb", 
        api_key = "287298112411797", 
        api_secret = "9QQ0JU44f7vucKqhAPY2FQrnRRg" 
    )
    bootstrap.init_app(app)
    mysql.init_app(app)
    CSRFProtect(app)

    from .student import user_bp as user_blueprint
    app.register_blueprint(user_blueprint)


    return app
