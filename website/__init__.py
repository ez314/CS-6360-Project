from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'onlineAuction_CS6360'

    from .views import views
    from .auth import auth
    from .productDetail import prodDetail

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(prodDetail)

    return app

