from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()


def create_app() -> Flask:
    from api.routes import blueprint
    import api.models

    app = Flask(__name__)
    app.register_blueprint(blueprint, url_prefix="/api/v1")
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://username:password@postgres:5432/ok-shop"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app, origins=["http://localhost:4200", "http://127.0.0.1:8080"])
    return app
