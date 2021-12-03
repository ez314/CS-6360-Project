import json
import website.database

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, column


def create_app():
    # Load configurations from file
    config = json.load(open('config.json', 'r'))
    mysql_server = config['mysql_server']
    mysql_db = config['mysql_db']
    mysql_username = config['mysql_username']
    mysql_password = config['mysql_password']

    sqlalchemy_uri = f'mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_server}/{mysql_db}'

    # Create and configure the flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'onlineAuction_CS6360'
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Import all the routes
    from .views import views
    from .auth import auth
    from .productDetail import prodDetail
    from .sell import sell
    from .profile import profile
    from .search import searchCategory
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(prodDetail)
    app.register_blueprint(sell)
    app.register_blueprint(profile)
    app.register_blueprint(searchCategory)

    # Initialize the database and start a session
    database.db = SQLAlchemy(app)

    # Inject context for categories, since these need to be fetched at every load
    @app.context_processor
    def inject_categories():
        statement = 'SELECT * FROM Category;'
        category_query_res = database.db.session.execute(text(statement)).all()
        return {
            'categories': [item['Name'] for item in category_query_res]
        }

    return app
