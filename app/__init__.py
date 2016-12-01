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

    import re
    from jinja2 import evalcontextfilter, Markup, escape

    _paragraph_re = re.compile(r'(?:\r){2,}')

    # FIXME: TEMP - should be somewhere else
    @app.template_filter()
    @evalcontextfilter
    def nl2br(eval_ctx, value):
        result = u'\n\n'.join(u'%s' % p.replace('\n', '<br>\n') for p in _paragraph_re.split(escape(value)))
        if eval_ctx.autoescape:
            result = Markup(result)
        return result

    return app
