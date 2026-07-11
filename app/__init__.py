from flask import Flask
from flask_cors import CORS
from config import Config
from app.extensions import db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from app.views import main
    app.register_blueprint(main)

    from app.api.routes import api
    app.register_blueprint(api)

    from app.admin.routes import admin
    app.register_blueprint(admin, url_prefix='/admin')

    with app.app_context():
        from app import models

    return app
