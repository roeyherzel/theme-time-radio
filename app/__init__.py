from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Create an application instance."""
    app = Flask(__name__)

    # import configuration
    # cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    # app.config.from_pyfile(cfg)
    app.config.from_object('config')

    # initialize extensions
    db.init_app(app)

    # import blueprints
    from .main import main as main_blueprint
    from .api import api_bp as api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)

    return app
