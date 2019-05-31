DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "youtube-yiwei"
#SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/tracks.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

import os
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
DATABASE_NAME = 'msia423ywzhang'
SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".\
format(conn_type, user, password, host, port, DATABASE_NAME)
