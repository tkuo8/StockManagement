# from flask_mysql_connector import MySQL
from flask_cors import CORS

# mysql = MySQL()

def init_cors(app):
    CORS(app)