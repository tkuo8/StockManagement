from flask import Flask
from .database import db, migrate
from .extensions import init_cors
from .api import bp
from .util import convert_keys_to_camel_case
import json, pdb


def create_app():
    app = Flask(__name__)

    # アプリ設定
    app.config.from_object("app.config.Config")

    # SQLAlchemyの初期化
    db.init_app(app)

    migrate.init_app(app, db)

    # CORS初期化
    init_cors(app)

    # Blueprint登録
    app.register_blueprint(bp)

    return app
