from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    DATABASE = os.getenv('DB_NAME', 'dbname')
    
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE}'  # SQLite 使用例
    SQLALCHEMY_TRACK_MODIFICATIONS = False           # 余計な警告を防ぐ