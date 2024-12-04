import os
from flask import Flask
from blueprints.users.models import login_manager, db
from blueprints.users.views import users as users_blueprint
from blueprints.inventory.views import inventory as inventory_blueprint
from blueprints.menus.views import menus as menus_blueprint
from blueprints.shopping.views import shopping as shopping_blueprint
from blueprints.wasted.views import wasted as wasted_blueprint
import config
if os.environ.get('MY_NAME') == 'makaniaizu' or os.environ.get('FLASK_ENV') == 'production':
    import psycopg2
    from flask_migrate import Migrate


def create_app():
    _app = Flask(__name__)
    _app.config.from_object(config)
    _app.register_blueprint(users_blueprint, url_prefix='/')
    _app.register_blueprint(inventory_blueprint, url_prefix='/inventory')
    _app.register_blueprint(menus_blueprint, url_prefix='/menus')
    _app.register_blueprint(shopping_blueprint, url_prefix='/shopping')
    _app.register_blueprint(wasted_blueprint, url_prefix='/wasted')
    login_manager.init_app(_app)
    login_manager.login_view = 'users.login'
    login_manager.login_message = 'ページにアクセスするにはログインしてください'
    db.init_app(_app)
    if os.environ.get('MY_NAME') == 'makaniaizu' or os.environ.get('FLASK_ENV') == 'production':
        Migrate(_app, db, compare_type=True, compare_server_default=True)
    with _app.app_context():
        db.create_all()
    return _app


app = create_app()
if __name__ == "__main__":
    app.run()
