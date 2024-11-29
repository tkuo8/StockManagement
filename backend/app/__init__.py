from flask import Flask
from .extensions import init_cors
from .routes import main

def create_app():
    app = Flask(__name__)

    # アプリ設定
    # app.config.from_object('app.config.Config')

    # MySQLの初期化
    # mysql.init_app(app)
    
    # CORS初期化
    init_cors(app)

    # Blueprint登録
    app.register_blueprint(main)

    return app
