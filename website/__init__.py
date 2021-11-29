import json
import website.database

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, column


def create_app():
    config = json.load(open('config.json', 'r'))
    mysql_server = config['mysql_server']
    mysql_db = config['mysql_db']
    mysql_username = config['mysql_username']
    mysql_password = config['mysql_password']

    sqlalchemy_uri = f'mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_server}/{mysql_db}'

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'onlineAuction_CS6360'
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    from .views import views
    from .auth import auth
    from .productDetail import prodDetail
    from .profile import profile

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(prodDetail)
    app.register_blueprint(profile)

    database.db = SQLAlchemy(app)
    print('database test:', database.db.session.execute((text('SELECT * FROM ONLINE_AUCTION.Buyer;'))).all())

    return app

