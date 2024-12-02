from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    USERNAME = os.getenv('DB_USERNAME', 'default_user')  # 環境変数が設定されていない場合のデフォルト値
    PASSWORD = os.getenv('DB_PASSWORD', 'default_pass')
    HOST = os.getenv('DB_HOST', 'localhost')
    DATABASE = os.getenv('DB_NAME', 'dbname')
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
