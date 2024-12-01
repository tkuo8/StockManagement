from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# SQLAlchemyのインスタンスを作成
db = SQLAlchemy()

def init_cors(app):
    CORS(app)