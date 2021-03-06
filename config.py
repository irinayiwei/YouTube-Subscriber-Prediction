import os

# local: export SQLALCHEMY_DATABASE_URI='sqlite:///data/database/churn_prediction.db'
# rds: export SQLALCHEMY_DATABASE_URI="{conn_type}://{user}:{password}@{host}:{port}/{DATABASE_NAME}"

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 9044
APP_NAME = "youtube-yiwei"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
MAX_ROWS_SHOW = 100

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
DATABASE_NAME = 'msia423ywzhang'
SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.format(conn_type=conn_type, user=user, password=password, host=host, port=port, DATABASE_NAME=DATABASE_NAME)



# # SQLALCHEMY_DATABASE_URI = os.environ.get("{}://{}:{}@{}:{}/{}").\
# # format(conn_type=conn_type, user, password, host, port, DATABASE_NAME)
# SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI").\
# format(conn_type=conn_type, user, password, host, port, DATABASE_NAME)
