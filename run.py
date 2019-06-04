"""Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

Current commands enabled:

To create a database for Channel:

    `python run.py create --channelID=93821, --channelDays=2974, --viewCount=372242, --likes=48282, --dislikes=38271, --videoCount=382, --commentCount=7625"`

To add a song to an already created database:

    `python run.py ingest --channelID=72514, --channelDays=72614, --viewCount=74625, --likes=25662, --dislikes=57532 --videoCount=211, --commentCount=8865"`

"""
import argparse
import logging.config
from app.app import app

logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("youtube-yiwei")
logger.debug('Test log')

from src.addChannel import create_db, add_channel
from src.loadData import run_loading
from src.generateFeatures import run_features
from src.trainModel import run_training
from src.scoreModel import run_score
from predictNew import run_predict

def run_app(args):
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the model source code")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create", description="Create database")
    sb_create.add_argument("--channelID", default="18329", help="random channel id")
    sb_create.add_argument("--channelDays", default="103", help="Days the channel has been created")
    sb_create.add_argument("--viewCount", default="48729", help="Total views of the channel")
    sb_create.add_argument("--likes", default="8728", help="Total likes of the channel")
    sb_create.add_argument("--dislikes", default="2637", help="Total dislikes of the channel")
    sb_create.add_argument("--commentCount", default="3728", help="Total comments of the channel")
    sb_create.add_argument("--videoCount", default="347", help="Total videos of the channel")
    sb_create.add_argument("--truncate", "-t", default=False, action="store_true",
                        help="If given, delete current records from YouTube table before create_all "
                             "so that table can be recreated without unique id issues ")
    sb_create.set_defaults(func=create_db)

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--channelID", default="12313", help="random channel id")
    sb_ingest.add_argument("--channelDays", default="736", help="Days the channel has been created")
    sb_ingest.add_argument("--viewCount", default="528920", help="Total views of the channel")
    sb_ingest.add_argument("--likes", default="96372", help="Total likes of the channel")
    sb_ingest.add_argument("--dislikes", default="19438", help="Total dislikes of the channel")
    sb_ingest.add_argument("--commentCount", default="28475", help="Total comments of the channel")
    sb_ingest.add_argument("--videoCount", default="769", help="Total videos of the channel")
    sb_ingest.add_argument("--truncate", "-t", default=False, action="store_true",
                        help="If given, delete current records from YouTube table before create_all "
                             "so that table can be recreated without unique id issues ")
    sb_ingest.set_defaults(func=add_channel)


    # ### Need to change below for my own codes ###
    # sb_load = subparsers.add_parser("load_data", description="Load data into a dataframe")
    # sb_load.add_argument('--config', help='path to yaml file with configurations')
    # sb_load.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    # sb_load.set_defaults(func=run_loading)

    # # FEATURE subparser
    # sb_features = subparsers.add_parser("generate_features", description="Generate features")
    # sb_features.add_argument('--config', help='path to yaml file with configurations')
    # sb_features.add_argument('--input', default=None, help="Path to CSV for input to model scoreing")
    # sb_features.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    # sb_features.set_defaults(func=run_features)

    # # TRAIN subparser
    # sb_train = subparsers.add_parser("train_model", description="Train model")
    # sb_train.add_argument('--config', help='path to yaml file with configurations')
    # sb_train.add_argument('--input', default=None, help="Path to CSV for input to model training")
    # sb_train.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    # sb_train.set_defaults(func=run_training)

    # # SCORE subparser
    # sb_score = subparsers.add_parser("score_model", description="Score model")
    # sb_score.add_argument('--config', help='path to yaml file with configurations')
    # sb_score.add_argument('--input', default=None, help="Path to CSV for input to model scoring")
    # sb_score.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    # sb_score.set_defaults(func=run_score)

    sb_run = subparsers.add_parser("app", description="Run Flask app")
    sb_run.set_defaults(func=run_app)

    args = parser.parse_args()
    args.func(args)