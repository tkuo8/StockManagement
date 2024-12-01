from flask import Flask
from .extensions import init_cors, db
from app.routes import api

def create_app():
    app = Flask(__name__)

    # アプリ設定
    app.config.from_object('app.config.Config')

    # SQLAlchemyの初期化
    db.init_app(app)
    
    # CORS初期化
    init_cors(app)

    # Blueprint登録
    app.register_blueprint(api.bp)

    return app
