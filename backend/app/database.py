from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# データベースとマイグレーションのインスタンス
db = SQLAlchemy()
migrate = Migrate()