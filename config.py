import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('host')
username = os.getenv('username')
password = os.getenv('password')
database = os.getenv('database')
secretkey = os.getenv('secretkey')
uploadfolder = os.path.join(os.getcwd(),"datafiles")

class Config():
    JSON_AS_ASCII=False
    TEMPLATES_AUTO_RELOAD=True
    JSON_SORT_KEYS = False
    SECRET_KEY = secretkey.encode(encoding="utf-8")
    JSONIFY_PRETTYPRINT_REGULAR = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{host}:3306/{database}"
    ENV = 'development'
    UPLOAD_FOLDER = uploadfolder
    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     "pool_pre_ping": True,
    #     "pool_recycle": 300,
    #     'pool_timeout': 600,
    #     'pool_size': 10,
    #     'max_overflow': 5,
    # }