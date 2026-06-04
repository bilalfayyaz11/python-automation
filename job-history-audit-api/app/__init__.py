from flask import Flask
from app.models import db
from app.config import Config


def create_app(config_class=Config):
    """
    Application factory pattern.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes import api
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    return app
